from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.template import RequestContext
from .models import Greeting
import json
import urllib2
import operator

# Use session to save information computed from ginger test api
# Homepage, records the timestamp if someone clicks, can direct to page1, page2, page3
def index(request):
    greeting = Greeting()
    greeting.save()
    return render(request, 'index.html')

# page1 displays a list of the upcoming events
# x3 key: vendor_name, value: (vid, vfrequency)
def vendors(request):
    if "v_dic_i" not in request.session:
        rankVendor(request)
    x2 = request.session["v_dic_i"]
    x4 = request.session["v_dic"]
    x3 = []
    for vname,index in x2.items():
        freq = x4[vname]
        x3.append((vname,index,freq))
    return render(request, 'vendors.html', {'data': x3})


# page2 displays a list of all vendors and how many events they have appeared over last 2 years,
# across all locations, with most frequent ones first
def events(request):
    if "v_dic_i" not in request.session:
        rankVendor(request)
    x = request.session["e_dic"]
    newx = {}
    for k,v in x.items():
        newx[k] = v[0]
    return render(request, 'allevent.html', {'data': newx.iteritems()})

# page3 displays all records of homepage visits
def db(request):
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})

# For a specific vendor, displays its name and the number of occurrences over the past 2 years
def v(request,vid):
    if "v_dic_i" not in request.session:
        rankVendor(request)
    x2 = request.session["r_dic_i"]
    vname = x2[vid]
    x = request.session["v_dic"]
    return render(request, 'v.html', {'vf': x[vname],'vn':vname})

# For a specific event, displays the vendors at the event
def event(request,id):
    if "v_dic_i" not in request.session:
        rankVendor(request)
    x = request.session["e_dic"]
    allv = x[id][1]
    newlist = []
    x2 = request.session["v_dic_i"]
    for v in allv:
        newlist.append((v,x2[v]))
    return render(request, 'allvendor.html', {'data': newlist})

# Below are two helper functions
# Go through all events, construct dictionaries and save in sessions for late usage
# e_dic: key:event_id, value:(event_name,[vendors])
# v_dic: key:vendor_name, value:vendor_occurance_num)
# v_dic_i_vname(v_dic_i): key:vendorname, value:rank(unique) (rank all vendors based on numbers of occurance)
# r_dic_i_vname(r_dic_i): same as v_dic_i_vname, except key, value are reversed
def rankVendor(request):
    i = 9
    j = 1
    e_dic = {}
    v_dic = {}
    v_dic_i_vname = {}
    r_dic_i_vname = {}
    while j < i:
        getJson(e_dic, j)
        j = j + 1
    for k,v in e_dic.items():
        for vv in v[1]:
            if vv not in v_dic:
                v_dic[vv] = 1
            else:
                v_dic[vv] += 1
    sortedl = sorted(v_dic.items(), key=operator.itemgetter(1),reverse=True)
    index = 0
    for sl in sortedl:
        v_dic_i_vname[sl[0]] = index
        r_dic_i_vname[index] = sl[0]
        index = index + 1
    request.session['e_dic'] = e_dic
    request.session['v_dic'] = v_dic
    request.session['v_dic_i'] = v_dic_i_vname
    request.session['r_dic_i'] = r_dic_i_vname

# For each event, return (event_name, [vendor1, vendor2,...]), use Ginger test api
def getJson(e_dic, event_id):
    f = urllib2.urlopen('https://ginger.io/test-project/events/' + str(event_id))
    j = json.loads(f.read())
    e_dic[event_id] = (j['data']['name'],j['data']['vendors_list'])