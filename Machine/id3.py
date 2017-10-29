 '''Kostas Kopanidis p3130098
  Xrusa Mauraki p3130128
 Lefteris Xatziarapis p3130255
 '''
from random import shuffle
import math


def read_data(file_path, shuffled=True):
    raw_data = None
    with open(file_path) as f:
        raw_data = [line.strip().split(',') for line in f]
        if shuffled:
            shuffle(raw_data)
    if raw_data is None:
        print("Incorrect file given")
        exit(1)

    return raw_data


def split_train_test(test_percent, data):
    train_size = int(len(data) * (1.0 - test_percent))
    train_data = list()
    test_data = list()
    for i in range(train_size):
        train_data.append(data[i])
    for i in range(train_size, len(data)):
        test_data.append(data[i])
    return train_data, test_data

def data_mapping(file):
    names= open(file)
    index_mapping=dict() # a dict with 2 keys  the column (category) and its value as string and the value of the dict will be the value as index
    value_to_index=dict() # a dict with 2 keys the column(category) and its value as index and value will be the value as string
    possible_column_values = list()
    splitter=":"
    answers=list()
    name_rows=list()
    for line in names:
        if splitter in line:
            name_rows.append(line.split(splitter)[-1].split(".")[0])
        else:
            if line != "\n" and "," in line:
                answers.append(line.split(","))

    for cat in range(len(name_rows) +1):
        possible_column_values.append({0})
        catnum=0
    for cat in name_rows:
        index = 0
        v= cat.split(",")
        for i in v:
            i=" ".join(i.split())
            index_mapping[catnum, i]= index
            value_to_index[catnum,index ]= i
            possible_column_values[catnum].add(index)
            index += 1
        catnum += 1
    index=0
    for j in answers:
        for i in j:
            i=" ".join(i.split())
            index_mapping[catnum, i ]= index
            value_to_index[catnum, index] = i
            possible_column_values[catnum].add(index)
            index += 1
    return index_mapping, value_to_index, possible_column_values



def dataHandler(data,index_mapping=None,value_to_index=None,possible_column_values=None):
    index_list = list() #a list with each row of data as a list of index values
    if index_mapping is None:
        index_mapping=dict() # a dict with 2 keys  the column (category) and its value as string and the value of the dict will be the value as index
        value_to_index=dict() # a dict with 2 keys the column(category) and its value as index and value will be the value as string
        possible_column_values = list()
        for cat in range(len(data[0])):
            possible_column_values.append({0})

        for cat in range(len(data[0])):
            index= -1
            for row in range(len(data)):
                if (cat, data[row][cat]) not in index_mapping:
                    index += 1
                    index_mapping[(cat, data[row][cat])] = index
                    value_to_index[(cat, index)] = data[row][cat] #if we want to find the value of an index later on
                    possible_column_values[cat].add(index)

        # now create the index list
    for row in range(len(data)):
        index_list.append(list())
        for cat in range(len(data[0])):
            index_list[row].append(index_mapping[cat, data[row][cat]])
    return index_list, index_mapping, value_to_index, possible_column_values


def print_accuracy(test_data,answers):
    counter=0
    for row in range (len(test_data)):
        if test_data[row][-1] == answers[row]:
            counter += 1
    acc = counter/len(test_data)
    print("Mean accuracy ")
    print(acc)


def print_precision_recall(test_data,answers,possible_answers_value):
    true_positive= dict()
    false_positive = dict()
    false_negative= dict()

    for p in possible_answers_value:
        true_positive[p]=0
        false_negative[p]=0
        false_positive[p]=0
    for row in range(len(test_data)):
        for p in possible_answers_value:
            if test_data[row][-1]== p and p == answers[row]:
                true_positive[p] +=1
            if p == answers[row] and test_data[row][-1] != p:
                false_positive[p] +=1
            if test_data[row][-1] == p and p !=answers[row]:
                false_negative[p] +=1

    precision= dict()
    recall= dict()
    psum=0
    rsum=0
    for p in possible_answers_value:
        if true_positive[p]==0:
            precision[p] = 0
            recall[p] =0
        else:
            precision[p] = true_positive[p] / (true_positive[p] + false_positive[p])
            psum += precision[p]
            recall[p] = true_positive[p] / (true_positive[p] + false_negative[p])
            rsum += recall[p]
    print("Precision for each class ")
    print(precision)
    print("Mean precision ")
    print(psum/(len(possible_answers_value)))
    print("Recall for each class ")
    print(recall)
    print("Mean recall ")
    print(rsum /(len(possible_answers_value)))


def H(array_count):
    h = 0
    total = sum(array_count)
    for i in range(0, len(array_count)):
        if array_count[i] > 0:
            h += -(array_count[i]/total * math.log2(array_count[i]/total))
    return h


def IG(train_data, possible_column_values, col, starting_h):
    answers = list([ans[-1] for ans in train_data])
    s = 0
    values_count = list()
    for i in range(len(possible_column_values[col])):
        values_count.append(0)
    # for every possible value of the column
    for i in range(len(train_data)):
        values_count[train_data[i][col]] += 1
    for i in range(len(values_count)):
        # calculate its probability
        prob = values_count[i] / sum(values_count)
        # create a conditional array count to measure the conditional entropy
        conditional_array_count = list()
        # initialize to zero with the size of the results
        for x in range(len(possible_column_values[-1])):
            conditional_array_count.append(0)
        for j in range(len(answers)):
            # we count only the training categories where the value matches
            if train_data[j][col] == i:
                conditional_array_count[answers[j]] += 1
        h = H(conditional_array_count)
        s += prob * h
    assert (starting_h - s >= 0)
    return starting_h - s


def predict(tree, test_data, value_to_index):
    answers_text = list()
    answers_ind = list()
    for row in range(len(test_data)):
        col = (len(test_data[row])-1)
        ans_ind = recursive_traverse(tree, test_data[row])
        ans_t = value_to_index[col, ans_ind]
        answers_ind.append(ans_ind)
        answers_text.append(ans_t)
    return answers_ind,answers_text


def recursive_traverse(tree, test_data):

    if isinstance(tree, int):
        return tree
    for key in tree.keys():
        subtree = tree[key]
        return recursive_traverse(subtree[test_data[key]], test_data)


def create_id3(train_data, remaining_categories, possible_column_values, preselected,threshold): # to add possible values
    #remaining_categories must be a set not a list
    #takes data as an array with both examples and answers
    tree = dict()
    #map with the quantity of each answer
    ans_count = dict()
    answers = list([ans[-1] for ans in train_data])
    max_ig=0
    max_index=0
    if len(remaining_categories) == 0 or train_data is None:
        return preselected
    preselected_count = -1
    preselected = -1
    for i in range(len(answers)):
        if answers[i] in ans_count:
            ans_count[answers[i]] += 1
        else:
            ans_count[answers[i]]= 1

    #we find the starting entropy taking only the values of the map
    starting_h = H(list(ans_count.values()))
    # we find the most common answer to set it as preselected for the next calls
    # this will also stop if answers are 95% in one category to avoid overfitting
    for i, count in ans_count.items():
        if count/sum(ans_count.values()) > threshold:
            return i
        if count > preselected_count:
            preselected = i
            preselected_count = count


    # we find the next category to split
    for i in remaining_categories:
        cur_ig = IG(train_data,possible_column_values,i, starting_h)
        if cur_ig > max_ig:
            max_ig = cur_ig
            max_index = i

    remaining_categories.remove(max_index)
    tree[max_index] = dict()
    #for each subcategory we have its index and a list of the rows of the training data, this we how we split the data for next calls
    sub_categories= dict()
    for r_l, row in enumerate(train_data):

        if train_data[r_l][max_index] not in sub_categories:
           sub_categories[train_data[r_l][max_index]]=list()

        sub_categories[train_data[r_l][max_index]].append(row)
    #now we want to recursively call id3 to fill the tree
    for cat_value, data in sub_categories.items():
        tree[max_index][cat_value] = create_id3(data, remaining_categories.copy(), possible_column_values, preselected,threshold)
    for cat_value in possible_column_values[max_index]:
        if cat_value not in tree[max_index]:
            tree[max_index][cat_value] = preselected
    return tree








#data = read_data("car.data")
train_data= read_data("car_train20.data", False)
test_data= read_data("car_test20.data", False)

train_data10, train_datarest = split_train_test(0.9,train_data)
index_mapping,value_to_index,possible_column_values = data_mapping("car_train10.names")
index_list, _, _, _ = dataHandler(train_data10,index_mapping,value_to_index,possible_column_values)
index_listT, _, _, _ = dataHandler(test_data,index_mapping,value_to_index,possible_column_values)

remaining_cat = set()
for i in range(len(index_list[0])-1):
    remaining_cat.add(i)


tree = create_id3(index_list, remaining_cat, possible_column_values, 0, 0.8)

ans_ind, ans_text= predict(tree,index_listT,value_to_index)
print(ans_ind)
print(ans_text)

print_precision_recall(index_listT, ans_ind, possible_column_values[-1])
print_accuracy(index_listT,ans_ind)
print(len(test_data))
#print(len(train_data10))