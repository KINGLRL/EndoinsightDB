CREATE TABLE surveys (
      survey_id INT PRIMARY KEY,
      title VARCHAR(255),
      description TEXT,
      date DATE,
      first_question_id INT,
      last_question_id INT

);

CREATE TABLE input_type (
      type_id INT PRIMARY KEY,
      name VARCHAR(50)
    
);

CREATE TABLE questions (
      question_id INT PRIMARY KEY,
      question_text VARCHAR(255),
      type_id INT,
      survey_id INT,
      FOREIGN KEY (type_id) REFERENCES input_type(type_id),
      FOREIGN KEY (survey_id) REFERENCES surveys(survey_id)
    
);

CREATE TABLE options (
      option_id INT PRIMARY KEY,
      option_text VARCHAR(255),
      question_id INT,
      FOREIGN KEY (question_id) REFERENCES questions(question_id)
    
);

CREATE TABLE question_logic (
      logic_id INT PRIMARY KEY,
      parent_question_id INT,
      parent_option_id INT,
      child_question_id INT,
      FOREIGN KEY (parent_question_id) REFERENCES questions(question_id),
      FOREIGN KEY (child_question_id) REFERENCES questions(question_id)
    
);


CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    sex VARCHAR(10),
    nation VARCHAR(50),
    ID_number VARCHAR(18),
    birthday DATE,
    phone_number VARCHAR(20),
    family_member_phone_number VARCHAR(20),
    height INT,
    weight INT,
    homeplace VARCHAR(100),
    last_login_time TIMESTAMP
);

CREATE TABLE image_responses (
      image_responses_id INT PRIMARY KEY,
      time TIMESTAMP,
      input_image BYTEA,
      predict_image BYTEA,
      user_id VARCHAR(255),
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    
);

CREATE TABLE responses (
      response_id VARCHAR(255) PRIMARY KEY,
      time TIMESTAMP,
      user_id VARCHAR(255),
      survey_id INT,
      current_question_id INT,
      FOREIGN KEY (user_id) REFERENCES users(user_id),
      FOREIGN KEY (survey_id) REFERENCES surveys(survey_id) 
    
);

CREATE TABLE question_responses (
      question_response_id VARCHAR(255) PRIMARY KEY,
      answer TEXT,
      response_id VARCHAR(255),
      question_id INT,
      FOREIGN KEY (response_id) REFERENCES responses(response_id),
      FOREIGN KEY (question_id) REFERENCES questions(question_id) 
    
);

CREATE TABLE selected_option (
      selected_option_id VARCHAR(255) PRIMARY KEY,
      question_response_id VARCHAR(255),
      option_id INT,
      FOREIGN KEY (question_response_id) REFERENCES question_responses(question_response_id),
      FOREIGN KEY (option_id) REFERENCES options(option_id) 
    
);

CREATE TABLE lists (
      list_id VARCHAR(255) PRIMARY KEY,
      parent_question_id INT,
      child_question_id INT,
      response_id VARCHAR(255),
      FOREIGN KEY (parent_question_id) REFERENCES questions(question_id),
      FOREIGN KEY (child_question_id) REFERENCES questions(question_id),
      FOREIGN KEY (response_id) REFERENCES responses(response_id)
);
	
INSERT INTO surveys (survey_id, title, description, date, first_question_id, last_question_id) VALUES (1, '疾病预测问卷调查', '', '2023-11-03', 1, 66);

INSERT INTO input_type (type_id, name) VALUES (0, '填空'),
(1, '单选'),
(2, '多选');

INSERT INTO questions (question_id, question_text, type_id, survey_id) VALUES (1, '您的姓名是?', 0, 1),
(2, '您的性别是?', 1, 1),
(3, '您的民族是?', 0, 1),
(4, '您的身份证号是?', 0, 1),
(5, '您的出生年是?', 0, 1),
(6, '您的出生月是?', 0, 1),
(7, '您的出生日是?', 0, 1),
(8, '患者本人电话号码?', 0, 1),
(9, '家属称呼?', 0, 1),
(10, '家属电话号码?', 0, 1),
(11, '您的身高是?', 0, 1),
(12, '您的体重是?', 0, 1),
(13, '您是否长期居住于出生地?', 1, 1),
(14, '家庭住址（省市县街道小区）?', 0, 1),
(15, '长期居住地地区名称（省市县街道小区）?', 0, 1),
(16, '居住时长?', 1, 1),
(17, '出生地地区名称（省市县）?', 0, 1),
(18, '居住时长?', 1, 1),
(19, '您是否有过幽门螺旋杆菌（Hp）感染?', 1, 1),
(20, '确诊时间年?', 0, 1),
(21, '确诊时间月?', 0, 1),
(22, '是否根除?', 1, 1),
(23, '根除完成时间年?', 0, 1),
(24, '根除完成时间月?', 0, 1),
(25, '您是否有龋齿（虫牙）、缺齿、口臭?', 1, 1),
(26, '您的饮食口味偏好是?', 2, 1),
(27, '您是否存在以下饮食习惯?', 2, 1),
(28, '您吸烟吗?', 1, 1),
(29, '吸烟几年?', 0, 1),
(30, '平均每天几支?', 0, 1),
(31, '吸烟几年?', 0, 1),
(32, '平均每天几支?', 0, 1),
(33, '戒烟几年?', 0, 1),
(34, '您饮酒吗?', 1, 1),
(35, '饮酒几年?', 0, 1),
(36, '饮酒频率?', 1, 1),
(37, '平均每天多少ml?', 0, 1),
(38, '饮什么酒?', 0, 1),
(39, '饮酒几年?', 0, 1),
(40, '饮酒频率?', 1, 1),
(41, '平均每天多少ml?', 0, 1),
(42, '饮什么酒?', 0, 1),
(43, '戒酒几年?', 0, 1),
(44, '您是否有长期在吃的药物?', 1, 1),
(45, '药物具体名称?', 0, 1),
(46, '剂量?', 0, 1),
(47, '服用时间?', 0, 1),
(48, '服用原因?', 0, 1),
(49, '您现在是否患有以下某种疾病?', 2, 1),
(50, '您现在是否患有以下某种疾病?', 2, 1),
(51, '您过去是否患有以下某种疾病?', 2, 1),
(52, '您是否做过手术?', 1, 1),
(53, '疾病名称?', 0, 1),
(54, '手术时间（年）?', 0, 1),
(55, '手术时间（月）?', 0, 1),
(56, '手术方式?', 0, 1),
(57, '您的一级亲属中是否有人患过肿瘤?', 1, 1),
(58, '称谓（与本人关系）?', 0, 1),
(59, '肿瘤详细名称（仅*填写一级亲属）?', 0, 1),
(60, '您是否有确诊的精神疾病（如焦虑、抑郁等）?', 1, 1),
(61, '疾病具体名称?', 0, 1),
(62, '疾病严重程度?', 0, 1),
(63, '病程时间?', 0, 1),
(64, '治疗措施?', 0, 1),
(65, '目前状况?', 0, 1),
(66, '您自我评价精神压力情况是?', 1, 1);

INSERT INTO options (option_id, option_text, question_id) VALUES (1, '男', 2),
(2, '女', 2),
(3, '是', 13),
(4, '否', 13),
(5, '小于一个月', 16),
(6, '一个月到半年', 16),
(7, '半年到三年', 16),
(8, '三年以上', 16),
(9, '小于一个月', 18),
(10, '一个月到半年', 18),
(11, '半年到三年', 18),
(12, '三年以上', 18),
(13, '是', 19),
(14, '已根除', 22),
(15, '根除失败', 22),
(16, '未根除', 22),
(17, '否', 19),
(18, '不详', 19),
(19, '是', 25),
(20, '否', 25),
(21, '不详', 25),
(22, '高盐', 25),
(23, '高糖', 25),
(24, '高油', 25),
(25, '喜烫食', 25),
(26, '喜烟熏食物', 25),
(27, '喜油炸食物', 25),
(28, '喜腌菜', 25),
(29, '喜红肉或加工肉类', 25),
(30, '以上均无', 25),
(31, '长期不吃早餐', 25),
(32, '少食蔬果', 25),
(33, '饮食不规律', 25),
(34, '暴饮暴食', 25),
(35, '吃饭速度快', 25),
(36, '吃剩饭菜', 25),
(37, '以上均无', 25),
(38, '吸烟，未戒', 28),
(39, '吸过烟，已戒', 28),
(40, '从不吸烟', 28),
(41, '喝酒，未戒', 34),
(42, '经常', 36),
(43, '偶尔', 36),
(44, '以前喝，已戒', 34),
(45, '经常', 40),
(46, '偶尔', 40),
(47, '从不喝酒', 34),
(48, '不详', 34),
(49, '有', 44),
(50, '无', 44),
(51, '不详', 44),
(52, '高血压', 44),
(53, '冠心病', 44),
(54, '糖尿病', 44),
(55, '慢性阻塞性肺部疾病', 44),
(56, '慢性心力衰竭', 44),
(57, '慢性肾衰', 44),
(58, '甲亢', 44),
(59, '甲减', 44),
(60, '胃炎', 44),
(61, '消化性溃疡', 44),
(62, '胃食管反流病', 44),
(63, '胃癌', 44),
(64, '食管癌', 44),
(65, '炎症性肠病', 44),
(66, '结直肠癌', 44),
(67, '胰腺癌', 44),
(68, '肝炎', 44),
(69, '肝硬化', 44),
(70, '胃炎', 44),
(71, '消化性溃疡', 44),
(72, '胃食管反流病', 44),
(73, '胃癌', 44),
(74, '食管癌', 44),
(75, '炎症性肠病', 44),
(76, '结直肠癌', 44),
(77, '胰腺癌', 44),
(78, '有', 52),
(79, '无', 52),
(80, '不详', 52),
(81, '有', 57),
(82, '无', 57),
(83, '不详', 57),
(84, '是', 60),
(85, '否', 60),
(86, '非常大', 66),
(87, '有点大', 66),
(88, '一般', 66),
(89, '没有', 66),
(90, '不详', 66);

INSERT INTO question_logic (logic_id, parent_question_id, parent_option_id, child_question_id) VALUES (1, 1, 0, 2),
(2, 2, 2, 3),
(3, 2, 1, 3),
(4, 3, 0, 4),
(5, 4, 0, 5),
(6, 5, 0, 6),
(7, 6, 0, 7),
(8, 7, 0, 8),
(9, 8, 0, 9),
(10, 9, 0, 10),
(11, 10, 0, 11),
(12, 11, 0, 12),
(13, 12, 0, 13),
(14, 13, 3, 14),
(15, 13, 4, 15),
(16, 15, 0, 16),
(17, 16, 8, 17),
(18, 16, 7, 17),
(19, 16, 6, 17),
(20, 16, 5, 17),
(21, 17, 0, 18),
(22, 18, 12, 19),
(23, 18, 11, 19),
(24, 18, 10, 19),
(25, 18, 9, 19),
(26, 14, 0, 19),
(27, 19, 13, 20),
(28, 20, 0, 21),
(29, 21, 0, 22),
(30, 22, 14, 23),
(31, 23, 0, 24),
(32, 19, 18, 25),
(33, 19, 17, 25),
(34, 22, 16, 25),
(35, 22, 15, 25),
(36, 24, 0, 25),
(37, 25, 21, 26),
(38, 25, 20, 26),
(39, 25, 19, 26),
(40, 25, 30, 27),
(41, 25, 29, 27),
(42, 25, 28, 27),
(43, 25, 27, 27),
(44, 25, 26, 27),
(45, 25, 25, 27),
(46, 25, 24, 27),
(47, 25, 23, 27),
(48, 25, 22, 27),
(49, 25, 37, 28),
(50, 25, 36, 28),
(51, 25, 35, 28),
(52, 25, 34, 28),
(53, 25, 33, 28),
(54, 25, 32, 28),
(55, 25, 31, 28),
(56, 28, 38, 29),
(57, 29, 0, 30),
(58, 28, 39, 31),
(59, 31, 0, 32),
(60, 32, 0, 33),
(61, 28, 40, 34),
(62, 33, 0, 34),
(63, 30, 0, 34),
(64, 34, 41, 35),
(65, 35, 0, 36),
(66, 36, 42, 37),
(67, 36, 43, 38),
(68, 37, 0, 38),
(69, 34, 44, 39),
(70, 39, 0, 40),
(71, 40, 45, 41),
(72, 40, 46, 42),
(73, 41, 0, 42),
(74, 42, 0, 43),
(75, 34, 48, 44),
(76, 34, 47, 44),
(77, 43, 0, 44),
(78, 38, 0, 44),
(79, 44, 49, 45),
(80, 45, 0, 46),
(81, 46, 0, 47),
(82, 47, 0, 48),
(83, 44, 51, 49),
(84, 44, 50, 49),
(85, 48, 0, 49),
(86, 44, 59, 50),
(87, 44, 58, 50),
(88, 44, 57, 50),
(89, 44, 56, 50),
(90, 44, 55, 50),
(91, 44, 54, 50),
(92, 44, 53, 50),
(93, 44, 52, 50),
(94, 44, 69, 51),
(95, 44, 68, 51),
(96, 44, 67, 51),
(97, 44, 66, 51),
(98, 44, 65, 51),
(99, 44, 64, 51),
(100, 44, 63, 51),
(101, 44, 62, 51),
(102, 44, 61, 51),
(103, 44, 60, 51),
(104, 44, 77, 52),
(105, 44, 76, 52),
(106, 44, 75, 52),
(107, 44, 74, 52),
(108, 44, 73, 52),
(109, 44, 72, 52),
(110, 44, 71, 52),
(111, 44, 70, 52),
(112, 52, 78, 53),
(113, 53, 0, 54),
(114, 54, 0, 55),
(115, 55, 0, 56),
(116, 52, 80, 57),
(117, 52, 79, 57),
(118, 56, 0, 57),
(119, 57, 81, 58),
(120, 58, 0, 59),
(121, 57, 83, 60),
(122, 57, 82, 60),
(123, 59, 0, 60),
(124, 60, 84, 61),
(125, 61, 0, 62),
(126, 62, 0, 63),
(127, 63, 0, 64),
(128, 64, 0, 65),
(129, 60, 85, 66),
(130, 65, 0, 66);