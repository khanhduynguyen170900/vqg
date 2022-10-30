'''
annotate_sent = [{'index': 16,
  'form': 'Thủ_tướng',
  'posTag': 'N',
  'nerLabel': 'O',
  'head': 15,
  'depLabel': 'dob'},
 {'index': 17,
  'form': 'đầu_tiên',
  'posTag': 'A',
  'nerLabel': 'O',
  'head': 16,
  'depLabel': 'nmod'},
 {'index': 18,
  'form': 'của',
  'posTag': 'E',
  'nerLabel': 'O',
  'head': 16,
  'depLabel': 'nmod'},
 {'index': 21,
  'form': 'từ',
  'posTag': 'E',
  'nerLabel': 'O',
  'head': 16,
  'depLabel': 'tmp'}]
'''

# ---merge_all_by_key(annotate_sent, 'form')---> ['Thủ tướng', 'đầu tiên', 'của', 'từ']
from unittest import result


def merge_all_by_key(annotate_sent, key):
  if key == 'form':
    return [anno_s[key].replace('_', ' ') for anno_s in annotate_sent]
  return [anno_s[key] for anno_s in annotate_sent]

# annotate_text = {0: annotate_sent_0, 1: annotate_sent_1} --> [merge_all_by_key(annotate_sent_0, 'form'),
#                                                               merge_all_by_key(annotate_sent_1, 'form')]
def sentence_segmentation(annotate_text):
  sentences = []
  for key, annotate_sent in annotate_text.items():
    sent = merge_all_by_key(annotate_sent, 'form')
    sentences.append(" ".join(sent).strip())
  return sentences

# Tìm root trong annotate_sent
def find_root(annotate_sent):
  _sent = merge_all_by_key(annotate_sent, 'form')
  root = dependency_parsing_sent_one_level(annotate_sent, head_index=0)
  if len(root) > 1:
    raise ValueError(f"{_sent} has more than 1 root.")
  return root[0]

# Tìm các phần tử trong annotate_sent có head_index = head_index
# Trường hợp head_index == -1 => Tìm các con trực tiếp của root
def dependency_parsing_sent_one_level(annotate_sent, head_index=-1):
  if head_index == -1:
    head_index = find_root(annotate_sent)['index']
  
  result = []
  for anno_s in annotate_sent:
    if anno_s['index'] == head_index or anno_s['head'] == head_index:
      result.append(anno_s)
  return result

# Giống dependency_parsing_sent_one_level, nhưng đàu vào là paragraph,
# sẽ tách câu trước rồi gọi hàm dependency_parsing_sent_one_level
def dependency_parsing_para_one_level(annotate_para):
  dp_level_s = []
  sentences = sentence_segmentation(annotate_para)
  for key, annotate_sent in annotate_para.items():
    dp_level_s.append({'sentence': sentences[int(key)], 'parsing': dependency_parsing_sent_one_level(annotate_sent)})
  return dp_level_s

# Kiểm tra một thẻ <sub,Np<B-Per,> có trong pattern không
def check_p_in_csf(p, csf_split):
  for i, csf in enumerate(csf_split):
    p_copy = p.replace('<', '')
    p_copy = p_copy.replace('>', '')
    csf = csf.replace('<', '')
    csf = csf.replace('>', '')

    p_copy_ele = p_copy.split(',')
    csf_ele = csf.split(',')
    for j, ce in enumerate(csf_ele):
      if p_copy_ele[j] != '':
        if p_copy_ele[j].lower() != csf_ele[j].lower():
          break
      if j == len(csf_ele)-1:
        return i+1
  return -1

# Từ annotate_sent ra format giống pattern
def change_sentence_format(annotate_sent):
  result = []
  for anno_s in annotate_sent:
    result.append(f"<{anno_s['depLabel']},{anno_s['posTag']},{anno_s['nerLabel']},{anno_s['form']}>")
  return ' '.join(result)

# pattern_matching
def pattern_matching(pattern, annotate_sent):
  annotate_sent_dp = dependency_parsing_sent_one_level(annotate_sent)
  csf = change_sentence_format(annotate_sent_dp)

  pattern_split = pattern.split()
  csf_split = csf.split()

  blank = False
  current_index = 0
  for i in range(len(pattern_split)):
    if pattern_split[i] == '_':
      blank = True
    else:
      index_p_in_csf = check_p_in_csf(pattern_split[i], csf_split) # --> index pattern_split[i] in csf_split
      if index_p_in_csf == -1:
        return False
      else:
        if not blank:
          if index_p_in_csf != current_index:
            return False  
        blank = False
        current_index = index_p_in_csf
  return True

# Fill giá trị vào qa_pattern
def get_qa(qa_pattern, annotate_sent):
  annotate_sent_dp = dependency_parsing_sent_one_level(annotate_sent)

  convert_dp_word = {}
  for anno_s_dp in annotate_sent_dp:
    if anno_s_dp['depLabel'] == 'root':
      convert_dp_word['root'] = anno_s_dp['form'].replace('_', ' ')
    else:
      convert_dp_word[anno_s_dp['depLabel']] = ' '.join(merge_all_by_key(\
                                            get_list_dp_tree(annotate_sent, anno_s_dp['index']),\
                                            'form'))
  qa = qa_pattern.split(',')
  question = qa[0]
  answer = qa[1]
  
  question_split = question.split()
  for i, qs in enumerate(question_split):
    if qs in convert_dp_word.keys():
      question_split[i] = convert_dp_word[qs]
    
  answer_split = answer.split()
  for i, ans in enumerate(answer_split):
    if ans in convert_dp_word.keys():
      answer_split[i] = convert_dp_word[ans]

  return (' '.join(question_split), ' '.join(answer_split))

# Trả về các cây con của index trong annotate_sent
def get_list_dp_tree(annotate_sent, index):
  list_dp_tree = dependency_parsing_sent_one_level(annotate_sent, index)
  if len(list_dp_tree) == 1:
    return list_dp_tree
  result = []
  for ele_dp_tree in list_dp_tree:
    if ele_dp_tree['index'] == index:
      result += [ele_dp_tree]
    else:
      result += get_list_dp_tree(annotate_sent, ele_dp_tree['index'])
  return result

def question_generation(annotate_text, patterns, file_output='../../io/output.txt'):
    sentences = sentence_segmentation(annotate_text)
    # results = {}
    results = []
    for i, sent in enumerate(sentences):
        try:
            annotate_sent = annotate_text[i]
            qas = []
            for pattern_id, p in enumerate(patterns):
                p = p.split('|')
                pattern = p[0]
                qa_pattern = p[1]
                # qas = []
                if pattern_matching(pattern, annotate_sent):
                    question, answer = get_qa(qa_pattern, annotate_sent)
                    qas.append({'question': question, 'answer': answer, 'pattern_id': pattern_id})
                    #results[i] = {'sentence': sent, 'qas':qas}
                    #results.append({'sentence': sent, 'qas':qas})
            if len(qas) > 0:
              results.append({'sentence': sent, 'qas':qas})
        except:
            continue
    # with open(file_output, 'a+') as f:
    #     for i, sent in results.items():
    #         f.write(f"{sent['sentence']}\n\n")
    #         for qa in sent['qas']:
    #             f.write(f"{qa['question']} ----- {qa['answer']}\n")
    #         f.write(f"\n-----------------------------\n")
    return results