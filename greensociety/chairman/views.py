from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from .models import *
from random import *
from django.core.mail import send_mail

# Create your views here.

def home (request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            mall = Member.objects.count ()
            nall = Notice.objects.count ()
            eall = Event.objects.count ()
            all_post = Post.objects.all ()
            context = {
                'uid' : uid,
                'cid' : cid,
                'mall' : mall,
                'nall' : nall,
                'eall' : eall,
                'all_post' : all_post,
            }
            return render (request, 'chairman/index.html',context)
        else:
            if uid.role == 'member' :
                mid = Member.objects.get(user_id=uid)
                all_post = Post.objects.all ()
                context = {
                    'uid' : uid,
                    'mid' : mid,
                    'all_post' : all_post,
                }
                return render(request, "chairman/m-index.html",context) 
            return render (request, "chairman/login.html")
    else:
        return render (request, "chairman/login.html")

def login (request):
        if "email" in request.session:
            return HttpResponseRedirect(reverse('home'))
        else:
            if request.POST:
                email = request.POST['email']
                password = request.POST['password']
                try:
                    uid = User.objects.get(email = email)
                    if uid.role == 'chairman':
                        if uid.password == password:
                            cid = Chairman.objects.get(user_id = uid)
                            request.session['email'] = uid.email 
                            mall = Member.objects.count ()
                            nall = Notice.objects.count ()
                            eall = Event.objects.count ()
                            all_post = Post.objects.all ()
                            context = {
                                'uid' : uid,
                                'cid' : cid,
                                'mall' : mall,
                                'nall' : nall,
                                'eall' : eall,
                                'all_post' : all_post,
                            }
                            return render (request, "chairman/index.html",context)
                        else:
                            context = {
                               'e_msg' : "Invalid Password"
                            }
                            return render(request,"chairman/login.html",context)
                    else:
                        try:
                            uid = User.objects.get(email = email)
                            if uid.role == "member":
                                if uid.password == password:
                                    mid = Member.objects.get (user_id = uid)
                                    request.session['email'] = uid.email
                                    all_post = Post.objects.all ()
                                    context = {
                                        'uid' : uid,
                                        'mid' : mid,
                                        'all_post' : all_post,
                                    }
                                    return render (request, "chairman/m-index.html",context)
                                else:
                                    return render (request, "chairman/login.html")
                            return render (request, "chairman/login.html")
                        except:
                            context = {
                                'e_msg' : "Invalid Email"
                            }
                            return render(request,"chairman/login.html",context)          
                except:
                    context = {
                        'e_msg' : "Invalid Email"
                    }
                    return render(request,"chairman/login.html",context)
        return render(request,"chairman/login.html")


def logout (request):
    if "email" in request.session:
        del request.session['email']
        return render(request,"chairman/login.html")
    else:
        return HttpResponseRedirect(reverse('login'))

def add_member (request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            context = {
                'uid' : uid,
                'cid' : cid,
            }
            if request.POST:
                email = request.POST['email']
                passcode = request.POST['firstname'][-3:-1] + email[3:6]
                #  for data register or enter or store or add use create ()
                # in django which is use ORM (object reletional mapping)
                # here , we are using create() insted or insert ()
                user_id = User.objects.create(email = email,password = passcode,role = "member")
                mid = Member.objects.create(user_id = user_id,
                                            firstname = request.POST['firstname'],
                                            lastname = request.POST['lastname'],
                                            contact = request.POST['contact'],
                                            gender = request.POST['gender'],
                                            house_no = request.POST['house_no'],
                                            occupation = request.POST['occupation'],
                                            working_place = request.POST['working_place'],
                                            family_mambers = request.POST['family_mambers'],
                                            vehicale_details = request.POST['vehicale_details'],
                                            birthdate = request.POST['birthdate'])
                all_member = Member.objects.all()
                if mid:
                    send_mail("Green Society Password","Your Password is :~ "+str(passcode),"devangmandviya002@gmail.com",[email])
                    msg = " successfully Member created !! Please Check Gmail Account For Password"
                    context = {
                        'all_member' : all_member,
                        'msg' : msg,
                        'uid' : uid,
                        'cid' : cid,
                    }
                    return render (request, "chairman/all-member.html",context)
                else:
                    context = {
                        'uid' : uid,
                        'cid' : cid,
                    }
                    return render (request, "chairman/add-member.html",context)
            return render (request, "chairman/add-member.html",context)
        else:
            return render (request, "chairman/add-member.html",context)

def all_member (request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            all_member = Member.objects.all()
            context = {
                'uid' : uid,
                'cid' : cid,
                'all_member' : all_member,
            }
            return render (request, "chairman/all-member.html",context)
        else:
            if uid.role == 'member':
                mid = Member.objects.get(user_id = uid)
                profiles = Member.objects.exclude(pk=request.user.pk)
                all_member = Member.objects.all()
                context = {
                    'uid' : uid,
                    'mid' : mid,
                    'profiles' : profiles,
                    'all_member' : all_member,
                }
                return render (request, "chairman/m-all-member.html",context)
    else:
        return render (request, "chairman/login.html")           

def add_notice (request):
    if "email" in request.session:
        uid = User.objects.get(email =request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            if request.POST:
                title = request.POST['title']
                description = request.POST['description']
                if "pic" in request.FILES:
                    pic = request.FILES['pic']
                    nid = Notice.objects.create(user_id = uid,title = title,description = description,pic = pic)
                else:
                    nid = Notice.objects.create(user_id = uid,title = title,description = description)
                if nid :
                    n_msg = "Successfully Notice Uploaded"
                    context={
                        'uid' : uid,
                        'cid' : cid,
                        'n_msg' : n_msg,
                    }
                    return render (request, "chairman/add-notice.html",context)
            else:
                context = {
                    'uid' : uid,
                    'cid' : cid,
                }
                return render (request, "chairman/add-notice.html",context)
        else:
            if uid.role == 'member':
                mid = Member.objects.get(user_id = uid)
                if request.POST:
                    title = request.POST['title']
                    description = request.POST['description']
                    if "pic" in request.FILES:
                        pic = request.FILES['pic']
                        nid = Notice.objects.create(user_id = uid,title = title,description = description,pic = pic)
                    else:
                        nid = Notice.objects.create(user_id = uid,title = title,description = description)
                    if nid :
                        n_msg = "Successfully Notice Uploaded"
                        context={
                            'uid' : uid,
                            'mid' : mid,
                            'n_msg' : n_msg,
                        }
                        return render (request, "chairman/m-add-notice.html",context)
                else:
                    context = {
                        'uid' : uid,
                        'mid' : mid,
                    }
                    return render (request, "chairman/m-add-notice.html",context)
        
        
def my_profile (request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            if request.POST:
                cid.firstname = request.POST['firstname']
                cid.lastname = request.POST['lastname']
                cid.contact = request.POST['contact']
                cid.gender = request.POST['gender']
                cid.visting_time = request.POST['visting_time']
                if 'pic' in request.FILES:
                    cid.pic = request.FILES['pic']
                    cid.save()
            context = {
                'uid' : uid,
                'cid' : cid,
            }
            return render (request, "chairman/my-profile.html",context)
        else:
            if uid.role == 'member':
                mid = Member.objects.get(user_id = uid)
                if request.POST:
                    mid.firstname = request.POST['firstname']
                    mid.lastname = request.POST['lastname']
                    mid.contact = request.POST['contact']
                    mid.gender = request.POST['gender']
                    mid.house_no = request.POST['house_no']
                    mid.occupation = request.POST['occupation']
                    mid.working_place = request.POST['working_place']
                    mid.family_mambers = request.POST['family_mambers']
                    mid.vehicale_details = request.POST['vehicale_details']
                    if 'pic' in request.FILES:
                        mid.pic = request.FILES['pic']
                        mid.save()
                context = {
                    'uid' : uid,
                    'mid' : mid,
                }
                return render (request, "chairman/m-my-profile.html",context)

def specific_user (request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            specific_uid = Member.objects.get(id = pk)
            context = {
                'uid' : uid,
                'cid' : cid,
                'specific_uid' : specific_uid,
            }
            return render (request, "chairman/specific-profile.html",context)
        else:
            if uid.role == 'member':
                mid = Member.objects.get(user_id = uid)
                specific_uid = Member.objects.get(id = pk)
                context = {
                    'uid' : uid,
                    'mid' : mid,
                    'specific_uid' : specific_uid,
                }
                return render (request, "chairman/m-specific-profile.html",context)

def all_notice (request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            all_notice = Notice.objects.all()
            context = {
                'uid' : uid,
                'cid' : cid,
                'all_notice' : all_notice,
            }
            return render (request, "chairman/all-notice.html",context)
        else:
            if uid.role == 'member':
                mid = Member.objects.get(user_id = uid)
                all_notice = Notice.objects.all()
                context = {
                    'uid' : uid,
                    'mid' : mid,
                    'all_notice' : all_notice,
                }
                return render (request, "chairman/m-all-notice.html",context)
            

def add_event (request):
    if "email" in request.session: #this line for check someone already logged in or not
        uid = User.objects.get(email=request.session['email'])  #check who one logged in 
        if uid.role == "chairman":  # who check is logged in person is Chairman or not 
            cid = Chairman.objects.get(user_id = uid)  # fetch data from Chairman table
            if request.POST:
                title = request.POST['title']
                if "pic" in request.FILES and "video" not in  request.FILES:
                    ein = Event.objects.create(user_id = uid, title = title, description = request.POST['description'], 
                                            date_event = request.POST['date_event'],event_time = request.POST['event_time'], pic = request.FILES['pic'])
                else:
                    ein = Event.objects.create(user_id = uid, title = title, description = request.POST['description'], 
                                            date_event = request.POST['date_event'],event_time = request.POST['event_time'])
                if ein :
                    e_msg = "Successfully Event Uploaded"
                    context = {
                        'uid' : uid,
                        'cid' : cid,
                        'e_msg' : e_msg,
                    }
                    return render(request,"chairman/add-event.html",context)    
            else:
                context = {
                    'uid' : uid,
                    'cid' : cid,
                }
                return render(request,"chairman/add-event.html",context)
        else:
            if uid.role == "member":
                mid = Member.objects.get(user_id = uid)
                if request.POST:
                    title = request.POST['title']
                    if "pic" in request.FILES and "video" not in  request.FILES:
                        ein = Event.objects.create(user_id = uid, title = title, description = request.POST['description'], 
                                                date_event = request.POST['date_event'], event_time = request.POST['event_time'],pic = request.FILES['pic'])
                    else:
                        ein = Event.objects.create(user_id = uid, title = title, description = request.POST['description'], 
                                                date_event = request.POST['date_event'],event_time = request.POST['event_time'])
                    if ein :
                        e_msg = "Successfully Event Uploaded"
                        context = {
                            'uid' : uid,
                            'mid' : mid,
                            'e_msg' : e_msg,
                        }
                        return render(request,"chairman/m-add-event.html",context)    
                else:
                    context = {
                        'uid' : uid,
                        'mid' : mid,
                    }
                    return render(request,"chairman/m-add-event.html",context)
    else:  # no ones logged in brfore this operation
        return render(request,"chairman/login.html")

def all_event (request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            all_event = Event.objects.all()
            context = {
                'uid' : uid,
                'cid' : cid,
                'all_event' : all_event,
            }
            return render (request, "chairman/all-event.html",context)
        else:
            if uid.role == 'member':
                mid = Member.objects.get(user_id = uid)
                all_event = Event.objects.all()
                context = {
                    'uid' : uid,
                    'mid' : mid,
                    'all_event' : all_event,
                }
                return render (request, "chairman/m-all-event.html",context)
    else:
        return render (request, "chairman/login.html")

def post (request):
    if "email" in request.session:
        uid = User.objects.get(email =request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            if request.POST:
                name = request.POST['name']
                product = request.POST['product']
                option = request.POST['option']
                contact = request.POST['contact']
                price = request.POST['price']
                if "pic" in request.FILES:
                    pic = request.FILES['pic']
                    pid = Post.objects.create(user_id = uid,name = name,product=product,option = option, contact = contact,price = price,pic = pic)
                else:
                    pid = Post.objects.create(user_id = uid,name = name,product=product,option = option, contact = contact,price = price)
                if pid :
                    p_msg = "Successfully Post Uploaded"
                    context={
                        'uid' : uid,
                        'cid' : cid,
                        'p_msg' : p_msg,
                    }
                    return render (request, "chairman/post.html",context)
            else:
                context = {
                    'uid' : uid,
                    'cid' : cid,
                }
                return render (request, "chairman/post.html",context)
        else:
            mid = Member.objects.get(user_id = uid)
            if request.POST:
                name = request.POST['name']
                product = request.POST['product']
                option = request.POST['option']
                contact = request.POST['contact']
                price = request.POST['price']
                if "pic" in request.FILES:
                    pic = request.FILES['pic']
                    pid = Post.objects.create(user_id = uid,name = name,product=product,option = option, contact = contact,price = price,pic = pic)
                else:
                    pid = Post.objects.create(user_id = uid,name = name,product=product,option = option, contact = contact,price = price)
                if pid :
                    p_msg = "Successfully Post Uploaded"
                    context={
                        'uid' : uid,
                        'mid' : mid,
                        'p_msg' : p_msg,
                    }
                    return render (request, "chairman/m-post.html",context)
            else:
                context = {
                    'uid' : uid,
                    'mid' : mid,
                }
                return render (request, "chairman/m-post.html",context)
            
def delete_user (request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            duser = Member.objects.get(id=pk)
            duser.delete()
            return redirect('all-member')
        
def change_password (request):
        if "email" in request.session:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'chairman':
                cid = Chairman.objects.get (user_id = uid)
                if request.POST:
                    currentpassword = request.POST['currentpassword']
                    newpassword = request.POST['newpassword']
                    if uid.password == currentpassword :
                        uid.password = newpassword
                        uid.save ()
                        return redirect("logout")
                    context = {
                        'uid' : uid,
                        'cid' : cid,
                    }
                    return render (request, "chairman/my-profile.html",context)
                else:
                    context = {
                        'uid' : uid,
                        'cid' : cid,
                    }
                    return render (request, "chairman/my-profile.html",context)
            else:
                if uid.role == 'member':
                        mid = Member.objects.get (user_id = uid)
                        if request.POST:
                            currentpassword = request.POST['currentpassword']
                            newpassword = request.POST['newpassword']
                            if uid.password == currentpassword :
                                uid.password = newpassword
                                uid.save ()
                                return redirect("logout")
                            context = {
                                'uid' : uid,
                                'mid' : mid,
                            }
                            return render (request, "chairman/my-profile.html",context)
                        else:
                            context = {
                                'uid' : uid,
                                'mid' : mid,
                            }
                            return render (request, "chairman/my-profile.html",context)
            
def contact_list (request):
    if "email" in request.session:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == 'chairman':
                cid = Chairman.objects.get (user_id = uid)
                c_contact = Chairman.objects.all ()
                m_contact = Member.objects.all ()
                context = {
                    'cid' : cid,
                    'uid' : uid,
                    'm_contact' : m_contact,
                    'c_contact' : c_contact,
                }
                return render (request,"chairman/contact-list.html",context)
            else:
                if uid.role == 'member':
                    mid = Member.objects.get (user_id = uid)
                    c_contact = Chairman.objects.all ()
                    m_contact = Member.objects.all ()
                    context = {
                        'mid' : mid,
                        'uid' : uid,
                        'm_contact' : m_contact,
                        'c_contact' : c_contact,
                    }
                    return render (request,"chairman/m-contact-list.html",context)
                
def add_maintainance (request):
    if "email" in request.session:
        uid = User.objects.get (email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        if request.POST:
            title = request.POST['title']
            amount = request.POST['amount']
            duedate = request.POST['duedate']
            mall = Member.objects.all()
            for i in mall:
                sid = Member.objects.get(id = i.id)
                mid = Maintainance.objects.create(user_id = uid,member_id = sid,
                                                  title = title,amount = amount,duedate = duedate)
                send_mail("Maintainance","Pls Pay Your Maintainance Befor Due Date :" +str(mid.duedate),"devangmandviya002@gmail.com",[mid.member_id.user_id.email])
            context = {
                    'status' : "Successfully Maintainance Added",
                    'uid' : uid,
                    'cid' : cid,
            }
            return render (request, "chairman/add-maintainance.html",context)
        else:
            context = {
                'uid' : uid,
                'cid' : cid,
            }
            return render (request, "chairman/add-maintainance.html",context)            
    

def forgot_password (request):
    if request.POST:
        email = request.POST['email']
        otp = randint(1000,9999)
        try:
            uid = User.objects.get (email = email)
            uid.otp = otp
            uid.save ()
            send_mail("Forgot Password","Your OTP is "+str(otp),"devangmandviya002@gmail.com",[email])
            context = {
                'email' : email,
            }
            return render (request, "chairman/change-password-o.html",context)
        except:
            context = {
                'emsg' : "Invalid Email Address"
            }    
            return render (request,"chairman/forgot-password.html",context)
    return render (request,"chairman/forgot-password.html")    

def change_password_o (request):
    if request.POST:
        email = request.POST['email']
        print ("=======================================>>",email)
        otp = request.POST['otp']
        newpassword = request.POST['newpassword']
        confirmpassword = request.POST['confirmpassword']
        uid = User.objects.get(email = email)
        if str(uid.otp) == otp:
            if newpassword == confirmpassword:
                uid.password = newpassword
                uid.save()
                context = {
                    'email' : email,
                    'smsg' : "Password Successfully Changed",
                }
                return render (request,"chairman/login.html",context)
            else:
                emsg = "Invalid Password"
                context = {
                    'email' : email,
                    'emsg' : emsg,
                }    
                return render (request,"chairman/change-password-o.html",context)
        else:
            emsg = "Invalid OTP"
            context = {
                'email' : email,
                'emsg' : emsg,
            }    
            return render (request,"chairman/change-password-o.html",context)
    return render (request,"chairman/change-password-o.html")    

def all_maintainance (request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        cid = Chairman.objects.get (user_id= uid)
        mall = Maintainance.objects.all()
        total = 0
        for i in mall:
            total +=int(i.amount)
        context = {
            'uid' : uid,
            'cid' : cid,
            'mall' : mall,
            'total' : total,
        }
        return render (request, "chairman/all-maintainance.html",context)
    
def m_all_maintainance (request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        mid = Member.objects.get (user_id= uid)
        mall = Maintainance.objects.filter(member_id = mid)
        context = {
            'uid' : uid,
            'mid' : mid,
            'mall' : mall,
        }
        return render (request, "chairman/m-all-maintainance.html",context)   
    
def delete_notice (request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            dnotice = Notice.objects.get(id=pk)
            dnotice.delete()
            return redirect('all-notice')    
        
def delete_event (request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            devent = Event.objects.get(id=pk)
            devent.delete()
            return redirect('all-event')            