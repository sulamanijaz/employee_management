from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.db.models import Q
from forms import userform, addsubuser, addschedule
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from formtools.wizard.views import WizardView, SessionWizardView
from employee_management.emp_manage_app.models import User, EmployeeSchedule
from django.shortcuts import redirect


def index_home(request):

    return render_to_response('employee/index.html', {
        'request': request,
    }, RequestContext(request, {}))


def login_user(request):
    if request.method == 'POST':

        username = request.POST['email']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                variables = {
                    'form': userform
                }
                return render(request, 'employee/login.html', variables)
        else:
                # Bad login details were provided. So we can't log the user in.
                variables = {
                    'form': userform,
                    'message':"Email or password incorrect",
                    'email':username
                }
                return render(request, 'employee/login.html', variables)

                # The request is not a HTTP POST, so display the login form.
                # This scenario would most likely be a HTTP GET.
    else:
            # No context variables to pass to the template system, hence the
            # blank dictionary object...
            return render_to_response('employee/login.html', {
                'request': request, 'form': userform,
            }, RequestContext(request, {}))

@login_required
def user_home(request):

    user_object=User.objects.filter(parent_user=request.user.id)
    user_count = user_object.count()
    count = user_count + 1
    total_emp_to_add = int(request.user.no_of_employees)-int(user_count)

    return render_to_response('employee/home.html', {
        'request': request,'emp_to_add':total_emp_to_add ,
        'count':count ,'form': userform,
        'user_obj':user_object
    }, RequestContext(request, {}))


from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/home/')


class ContactWizard(SessionWizardView):
    template_name = 'employee/signup.html'

    def done(self, form_list, form_dict ,**kwargs):
        user_dict = []
        for form in form_list:
            user_dict.append(form.cleaned_data)
        user_object=User.objects.create_superuser(user_dict[0]['email'], user_dict[1]['password'], fullname=user_dict[0]['fullname'],
                                      no_of_employees=user_dict[1]['no_of_employees'], is_staff=False,
                                      time_zone='india', parent_user = 0)

        user = authenticate(username=user_object.email, password=user_dict[1]['password'])

        login(self.request, user)

        return redirect('/home/')

@login_required
def add_sub_user(request, msg=None):

    user_object = User.objects.filter(parent_user=request.user.id)
    user_count = user_object.count()
    count = user_count + 1
    total_emp_to_add = int(request.user.no_of_employees) - int(user_count)
    t_emp = int(request.user.no_of_employees)
    msgs=''
    if msg:
        msgs = msg
    if request.method == 'GET':
        return render_to_response('employee/addsubuser.html', {
            'request': request, 'form': addsubuser,'count':count,
            't_emp':t_emp,'msg':msgs
        }, RequestContext(request, {}))

    elif request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not addsubuser(request.POST).is_valid():
                return render_to_response('employee/addsubuser.html', {
                    'request': request, 'form': addsubuser(request.POST),'count':count,
                    't_emp':t_emp

                }, RequestContext(request, {}))
        else:
            User.objects.create_user(email, password, fullname=fullname,
                                      no_of_employees=0, is_staff=True,
                                      time_zone='india', parent_user = request.user.id,
                                     )
            return redirect('/add_user/')


@login_required
def emp_schedule(request):
    msg = ''
    user_object=User.objects.filter(parent_user=request.user.id)
    if request.method == 'POST':
        shift_starts=request.POST.get('shift_starts', None)
        shift_ends = request.POST.get('shift_ends', None)
        toBox_cats = request.POST.getlist('toBox_cats[]', None)
        availability = request.POST.get('availability', None)
        recurrance = request.POST.get('recurrance', None)
        shift_starts = datetime.strptime(shift_starts, "%Y-%m-%d %H:%M")
        shift_ends = datetime.strptime(shift_ends, "%Y-%m-%d %H:%M")

        if toBox_cats:
            emp_schedule_list = []
            for user in toBox_cats:
                emp_schedule_list.append(EmployeeSchedule(parent_user=User.objects.get(pk=request.user.id), shift_start=shift_starts,
                                                          shift_ends=shift_ends, employee_id=User.objects.get(pk=user), availability=availability)
                                         )
            EmployeeSchedule.objects.bulk_create([data for data in emp_schedule_list])

            msg = "Schedule For selected users has been created successfully."

    return render_to_response('employee/emp_schedule.html', {
        'request': request,'user_object':user_object ,'msg':msg,'form': addschedule(),


    }, RequestContext(request, {}))