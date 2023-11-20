import os
import json
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, jsonify
import image_process
from flask_cors import CORS
from utils.json_to_sql import json_to_sql
import hashlib

app = Flask(__name__)
CORS(app)


def check(cur, table, id_name, table_id):
    s = 'select %s from %s where %s.%s=' % (id_name, table, table, id_name)
    if type(table_id) == int:
        s = s + str(table_id)  # 如果table_id是整数，直接添加
    else:
        s = s + '\'' + table_id + '\'' # 如果table_id不是整数，添加引号后再添加
    cur.execute(s)
    res = cur.fetchall()
    # 检查查询结果，如果没有记录，返回0；否则返回1
    if(len(res) == 0):
        return 0
    else:
        return 1


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='endo',
                            user='endo',
                            password='123456')
    return conn


@ app.route('/api/surveys/<survey_id>/end_survey', methods=['POST'])
def end_survey(survey_id):
    response = request.get_json()
    survey_id = int(survey_id) # 将survey_id转换为整数
    conn = get_db_connection()
    cur = conn.cursor()
    response_id = response.get('response_id')
    user_id = response.get('user_id')
    # 检查survey_id, user_id, 和response_id是否在相应的数据库表中存在
    if(check(cur, 'surveys', 'survey_id', survey_id) == 0 or
       check(cur, 'users', 'user_id', user_id) == 0 or
       check(cur, 'responses', 'response_id', response_id) == 0
       ):
        cur.close()
        conn.close()
        error_info = {'type': 'InvalidData', 'description': '提供数据不正确'}
        return jsonify({'message': 'fail', 'error': error_info})   # 返回错误信息
    # todo
    return jsonify({'message': 'success'})  # 返回成功信息


@ app.route('/api/surveys/<survey_id>/questions/<question_id>/previous_question',
            methods=['POST'])
def getPreviousQuestion(survey_id, question_id):
    response = request.get_json()
    survey_id = int(survey_id)
    question_id = int(question_id)
    conn = get_db_connection()
    cur = conn.cursor()
    response_id = response.get('response_id')
    user_id = response.get('user_id')
    # 获取当前问题的 ID
    cur.execute('select current_question_id from responses'
                ' where responses.response_id=%s and responses.user_id=%s',
                (response_id, user_id)
                )
    current_question_id = cur.fetchall()[0][0]
    # 如果当前问题 ID 与请求中的问题 ID 不匹配，则返回错误信息
    if current_question_id != question_id:
        error_info = {'type': 'NoMatching', 'description': '问题编号不匹配'}
        return jsonify({'message': 'fail', 'error': error_info})

     # 获取上一个问题的 ID 和链表ID
    cur.execute('SELECT list_id, parent_question_id '
                'FROM lists '
                'WHERE lists.child_question_id=%s AND'
                ' lists.response_id=%s',
                (question_id, response_id)
                )
    cur_list = cur.fetchall()[0]
    list_id, previous_question_id = cur_list

    # 获取上一个问题的文本和类型
    cur.execute('select question_text, type_id from questions '
                'where questions.question_id=%s',
                (previous_question_id, )
                )
    cur_list = cur.fetchall()[0]
    question_text, type_id = cur_list

    # 获取上一个问题的选项
    cur.execute('select * from options '
                'where options.question_id=%s',
                (previous_question_id,)
                )
    cur_list = cur.fetchall()
    previous_question_options = cur_list
    option_num = len(previous_question_options)
    options_text = []
    for previous_question_option in previous_question_options:
        options_text.append(previous_question_option[1])
    
    # 获取之前选择的答案
    cur.execute('select * from question_responses '
                'where response_id=%s and question_id=%s',
                (response_id, previous_question_id)
                )
    question_response_before = cur.fetchall()[0]
    hist_text = question_response_before[1]
   
    # 获取之前选择的选项
    cur.execute('select * from selected_option '
                'where question_response_id=%s',
                (question_response_before[0], )
                )
    hist_options = []
    options_before = cur.fetchall()
    for option_before in options_before:
        hist_options.append(option_before[2])
    
    # 检查是否为第一个问题
    cur.execute('select first_question_id from surveys '
                'where survey_id=%s',
                (survey_id, )
                )
    first_question_id = cur.fetchall()[0][0]
    if first_question_id == previous_question_id:
        is_first_question = True
    else:
        is_first_question = False

    # 准备返回的数据
    data = {
        'question_id': previous_question_id,
        'question_text': question_text,
        'type_id': type_id,
        'option_num': option_num,
        'options_text': options_text,
        'hist_text': hist_text,
        'hist_options': hist_options,
        'is_first_question': is_first_question
    }
    
    # 更新链表
    cur.execute('delete from lists where list_id=%s',
                (list_id,)
                )
    conn.commit()

    # 更新当前问题编号
    cur.execute('update responses '
                'set current_question_id=%s'
                'where response_id=%s', (previous_question_id, response_id)
                )
    conn.commit()
    cur.close()
    conn.close()

    # 返回成功消息和数据
    return jsonify({'msg': 'success', 'data': data})


@ app.route('/api/surveys/<survey_id>/questions/<question_id>/next_question',
            methods=['POST'])
def getNextQuestion(survey_id, question_id):
    response = request.get_json()
    survey_id = int(survey_id)
    question_id = int(question_id)
    conn = get_db_connection()
    cur = conn.cursor()
    response_id = response.get('response_id')
    user_id = response.get('user_id')

    # 获取当前问题的 ID
    cur.execute('select current_question_id from responses'
                ' where responses.response_id=%s and responses.user_id=%s',
                (response_id, user_id)
                )
    current_question_id = cur.fetchall()
    current_question_id = current_question_id[0][0]

    # 如果当前问题 ID 与请求中的问题 ID 不匹配，则返回错误信息
    if current_question_id != question_id:
        error_info = {'type': 'NoMatching', 'description': '问题编号不匹配'}
        return jsonify({'message': 'fail', 'error': error_info})

    # 根据当前问题 ID 获取下一个问题的 ID
    if current_question_id == 0:
        # 如果当前问题 ID 为 0，则获取第一个问题的 ID
        cur.execute('select first_question_id from surveys where '
                    'surveys.survey_id={}'.format(survey_id,))
        first_question_id = cur.fetchall()
        next_question_id = first_question_id[0][0]
    else:
        # 否则，根据逻辑确定下一个问题的 ID
        cur.execute('select type_id from questions '
                    'where questions.question_id=%s',
                    (current_question_id, )
                    )
        type_id = cur.fetchall()[0][0]
        cur.execute('select question_response_id from question_responses '
                    'where response_id=%s and question_id=%s',
                    (response_id, current_question_id)
                    )
        question_response_id = cur.fetchall()[0][0]
        cur.execute('select option_id from selected_option '
                    'where question_response_id=%s',
                    (question_response_id, )
                    )
        cur_list = cur.fetchall()
        if cur_list:
            option_id = cur_list[0][0]
        else:
            option_id = 0
        cur.execute('SELECT Child_question_id '
                    'FROM Question_logic AS ql '
                    'WHERE ql.Parent_question_id=%s AND'
                    ' ql.Parent_option_id=%s',
                    (question_id, option_id)
                    )
        next_question_id = cur.fetchall()[0][0]

     # 获取下一个问题的详细信息
    cur.execute('select question_text, type_id from questions '
                'where questions.question_id=%s',
                (next_question_id, )
                )
    cur_list = cur.fetchall()
    question_text, type_id = cur_list[0]
    cur.execute('select * from options '
                'where options.question_id=%s',
                (next_question_id,)
                )
    next_question_options = cur.fetchall()
    option_num = len(next_question_options)
    options_text = []
    for next_question_option in next_question_options:
        options_text.append(next_question_option[1])

    # 获取之前提交的答案，如果有的话
    cur.execute('select * from question_responses '
                'where response_id=%s and question_id=%s',
                (response_id, next_question_id)
                )
    cur_list = cur.fetchall()
    question_response_before = ()
    if cur_list:
        question_response_before = cur_list[0]
    if len(question_response_before) == 0:
        submit_before = False
        hist_text = ''
        hist_options = []
    else:
        submit_before = True
        hist_text = question_response_before[1]
        cur.execute('select * from selected_option '
                    'where question_response_id=%s',
                    (question_response_before[0], )
                    )
        hist_options = []
        options_before = cur.fetchall()
        for option_before in options_before:
            hist_options.append(option_before[2])

    # 检查是否为最后一个问题
    cur.execute('select last_question_id from surveys '
                'where survey_id=%s',
                (survey_id, )
                )
    cur_list = cur.fetchall()
    last_question_id = cur_list[0][0]
    if last_question_id == next_question_id:
        is_last_question = True
    else:
        is_last_question = False

    # 准备返回的数据
    data = {
        'question_id': next_question_id,
        'question_text': question_text,
        'type_id': type_id,
        'option_num': option_num,
        'options_text': options_text,
        'submit_before': submit_before,
        'hist_text': hist_text,
        'hist_options': hist_options,
        'is_last_question': is_last_question
    }

    # 更改当前问题编号
    cur.execute('update responses '
                'set current_question_id=%s'
                'where response_id=%s', (next_question_id, response_id)
                )
    conn.commit()

    # 更新链表
    if current_question_id != 0:
        m = hashlib.sha256()
        question_id_encode = str(current_question_id).encode('utf-8')
        next_question_id_encode = str(next_question_id).encode('utf-8')
        response_id_encode = response_id.encode('utf-8')
        m.update(question_id_encode)
        m.update(next_question_id_encode)
        m.update(response_id_encode)
        list_id = m.hexdigest()
        list_ = []
        list_dict = {}
        list_dict['list_id'] = list_id
        list_dict['parent_question_id'] = current_question_id
        list_dict['child_question_id'] = next_question_id
        list_dict['response_id'] = response_id
        list_.append(list_dict)
        list_sql = json_to_sql({'lists': list_})
        cur.execute(list_sql)
        conn.commit()
    cur.close()
    conn.close()
    return jsonify({'msg': 'success', 'data': data})


@ app.route('/api/surveys/<survey_id>/questions/<question_id>/submit',
            methods=['POST'])
def submit(survey_id, question_id):
    response = request.get_json()
    survey_id = int(survey_id)
    question_id = int(question_id)
    user_id = response.get('user_id')
    response_id = response.get('response_id')
    type_id = response.get('type_id')
    conn = get_db_connection()
    cur = conn.cursor()

    # 检查是否在相应的数据库表中存在
    if(check(cur, 'surveys', 'survey_id', survey_id) == 0 or
       check(cur, 'questions', 'question_id', question_id) == 0 or
       check(cur, 'users', 'user_id', user_id) == 0 or
       check(cur, 'responses', 'response_id', response_id) == 0 or
       check(cur, 'input_type', 'type_id', type_id) == 0):
        cur.close()
        conn.close()
        error_info = {'type': 'InvalidData', 'description': '提供数据不正确'}
        return jsonify({'message': 'fail', 'error': error_info})

    # 检查是否有答案文本
    if not response.get('text'):
        error_info = {'type': 'EmptyData', 'description': '没有填写答案'}
        return jsonify({'message': 'fail', 'error': error_info})
    cur.execute('select current_question_id from responses'
                ' where responses.response_id=%s and responses.user_id=%s',
                (response_id, user_id)
                )
    current_question_id = cur.fetchall()
    current_question_id = current_question_id[0][0]

    # 检查当前问题 ID 是否匹配
    if current_question_id != question_id:
        error_info = {'type': 'NoMatching', 'description': '问题编号不匹配'}
        return jsonify({'message': 'fail', 'error': error_info})

    # 生成问题回应的唯一 ID
    m = hashlib.sha256()
    response_id_encode = response.get('response_id').encode('utf-8')
    question_id_encode = str(question_id).encode('utf-8')
    m.update(response_id_encode)
    m.update(question_id_encode)
    question_response_id = m.hexdigest()

    # 检查是否之前已提交过答案
    cur.execute('select question_response_id from question_responses '
                'where question_response_id=%s',
                (question_response_id,)
                )
    submit_before = cur.fetchall()
    if len(submit_before) != 0:
        # 如果之前提交过，则先删除旧的答案和选项
        cur.execute('begin transaction')
        conn.commit()
        cur.execute('delete from selected_option where '
                    'question_response_id=%s',
                    (question_response_id,)
                    )
        conn.commit()
        cur.execute('delete from question_responses where '
                    'question_response_id=%s',
                    (question_response_id,)
                    )
        conn.commit()

        # 插入新的答案
        question_response = {
            'question_response_id': question_response_id,
            'answer': response.get('text'),
            'response_id': response.get('response_id'),
            'question_id': question_id
        }
        response_list = []
        response_list.append(question_response)
        question_response_sql = json_to_sql({'question_responses':
                                             response_list})

        cur.execute(question_response_sql)
        conn.commit()
        cur.execute('commit transaction')
        conn.commit()
    else:
        question_response = {
            'question_response_id': question_response_id,
            'answer': response.get('text'),
            'response_id': response.get('response_id'),
            'question_id': question_id
        }
        response_list = []
        response_list.append(question_response)
        question_response_sql = json_to_sql({'question_responses':
                                             response_list})
        cur.execute(question_response_sql)
        conn.commit()
    
    # 如果问题类型是选择题，则插入选择的选项
    if response.get('type_id') == 1 or response.get('type_id') == 2:
        cur.execute('select row_to_json(t) from('
                    'select * from options where options.question_id=%s'
                    ' order by option_id ASC'
                    ') t', (question_id,))
        options = cur.fetchall()
        for option in response.get('selected_options'):
            m = hashlib.sha256()
            question_response_encode = question_response_id.encode('utf-8')
            option_id_encode = str(
                options[option][0].get('option_id')).encode('utf-8')
            m.update(question_response_encode)
            m.update(option_id_encode)
            selected_option_id = m.hexdigest()

            select_option = {
                'selected_option_id': selected_option_id,
                'question_response_id': question_response_id,
                'option_id': options[option][0].get('option_id')
            }
            response_list = []
            response_list.append(select_option)
            select_option_sql = json_to_sql(
                {'selected_option': response_list})
            cur.execute(select_option_sql)
            conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'success'})


@ app.route('/api/surveys/<survey_id>/new_survey_instance', methods=['POST'])
def createSurveyInstance(survey_id):
    response = request.get_json()
    survey_id = int(survey_id)
    user_id = response.get('user_id')
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 检查用户信息是否存在
    cur.execute('select row_to_json(t) from('
                'select * from users where users.user_id=%s'
                ') t', (user_id,))
    basic_info = cur.fetchall()
    if(len(basic_info) == 0):
        cur.close()
        conn.close()
        error_info = {'type': 'NoUserInfo', 'description': '无该用户'}
        return jsonify({'message': 'fail', 'error': error_info})

    # 生成唯一的 response_id
    m = hashlib.sha256()
    user_id = response.get('user_id').encode('utf-8')
    time = response.get('time').encode('utf-8')
    m.update(user_id)
    m.update(time)
    response_id = m.hexdigest()

    # 设置 response 的初始值
    response['current_question_id'] = 0
    response['survey_id'] = survey_id
    response['response_id'] = response_id
    response_list = []
    response_list.append(response)

    # 插入新的 response 记录
    response_sql = json_to_sql({'responses': response_list})
    cur.execute(response_sql)
    conn.commit()
    
    # 获取调查问卷的标题和描述
    cur.execute('select title, description from surveys where '
                'surveys.survey_id={}'.format(survey_id))
    cur_list = cur.fetchall()
    msg = {}
    msg['response_id'] = response_id
    msg['title'] = cur_list[0][0]
    msg['description'] = cur_list[0][1]

    cur.close()
    conn.close()
    return jsonify({'message': 'success', 'data': msg})


@ app.route('/api/basic_info', methods=['POST'])
def postBasicInfo():
    response = []
    response.append(request.get_json())

    # 将 response 列表转换为 SQL 语句，准备插入到 users 表中
    response_sql = json_to_sql({'users': response})
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(response_sql)
    conn.commit()

    cur.close()
    conn.close()
    return jsonify({'message': 'success'})


@ app.route('/api/basic_info/<user_id>', methods=['GET'])
def getBasicInfo(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # 执行 SQL 查询以获取指定用户 ID 的基本信息
    cur.execute('select row_to_json(t) from('
                'select * from users where users.user_id=%s'
                ') t', (user_id,))
    basic_info = cur.fetchall()
    # 检查是否找到了用户信息
    if(len(basic_info) == 0):
        cur.close()
        conn.close()
        error_info = {'type': 'NoUserInfo', 'description': '无该用户'}
        return jsonify({'message': 'fail', 'error': error_info}) # 如果没有找到用户，返回错误信息

    cur.close()
    conn.close()
    return jsonify({'message': 'seccess', 'data': basic_info})


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=9999)