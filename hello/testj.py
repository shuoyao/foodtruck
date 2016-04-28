import json
import urllib2
import operator


# def testj():
#     f = urllib2.urlopen('https://ginger.io/test-project/events')
#     j = json.loads(f.read())
#     v = j['data']
#     v1 = v[1]
#     v3 = v1["vendors_list"]
#     # v = v[0]
#     # v = v["vendors_list"]
#     # v = v[1]
#     # v = j['data']['vendors_list'][0]
#     print v3

def load(vname):
    vd = open('v_dic', 'r')
    x = json.load(vd)
    # return render(request, 'v.html', {'data': x[vname]})

    # sl = open('v_dic', 'r')
    # x = json.load(sl)
    # name,num = x[0]
    print x[vname]
    # print num
    print "end"




# Go through all events, find which vendor at event(e_dic), 
# and count each vendors' overall occurance and rank(v_dic)
# v_dic_i_vname: key is vendorname, value is its unique rank
def rankVendor():
    i = 3
    j = 1
    e_dic = {}
    v_dic = {}
    v_dic_i_vname = {}
    while j < i:
        getJson(e_dic, j)
        j = j + 1
    for k,v in e_dic.items():
        # print k
        # print v
        for vv in v[1]:
            if vv not in v_dic:
                v_dic[vv] = 1
            else:
                v_dic[vv] += 1
    sortedl = sorted(v_dic.items(), key=operator.itemgetter(1),reverse=True)
    index = 0
    for sl in sortedl:
        v_dic_i_vname[sl[0]] = index
        index = index + 1

    # for k,v in v_dic_i_vname.items():
    #     print k
    #     print v
    f = open('sortedl', 'w')
    json.dump(sortedl, f)
    f2 = open('v_dic', 'w')
    json.dump(v_dic, f2)

    return e_dic, sortedl

# For each event, return (event_name, [vendor1, vendor2,...])
def getJson(e_dic, event_id):
    f = urllib2.urlopen('https://ginger.io/test-project/events/' + str(event_id))
    j = json.loads(f.read())
    e_dic[event_id] = (j['data']['name'],j['data']['vendors_list'])

# rankVendor()
# load("Beach Brew")




    # print "e_dic is:"
    # print type(id)
    # if testmode:
    #     id = id.encode('ascii','ignore')
    # # # print type(id)
    #     id = int(id)
    # print id
    # print type(id)