surveys($\underline{survey\_type}$, title, description, date, first_question_id, last_question_id)

question_type_map($\underline{question\_type}$, name)

questions($\underline{question\_id}$, question_text,  **question_type**, **survey\_id**)

options($\underline{option\_id}$, option_text, **question_id**)

question_logic($\underline{logic\_id}$, parent_question_id, parent_option_id, child_question_id)

users($\underline{user\_id}$, name, sex, nation, ID_number, birthday, phone_number, family_member_phone_number, height, weight, homeplace, last_login_time)

image_responses($\underline{image\_responses\_id}$, time, input_image, predict_image, **user_id**)

responses($\underline{response\_id}$, time, **user_id**, **survey_id**, current_question_id)

question_answers($\underline{question\_answers\_id}$, answer, **response_id**, **question_id**)

selected_option($\underline{selected\_option\_id}$,  **question_answers_id**, **option_id**)

lists($\underline{list\_id}$, **parent_question_id**, **child_question_id**, **response_id**)

