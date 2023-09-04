from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime
from django.contrib import messages

# Create your views here.
@login_required
def add_timeoff(request):
    timeoff_types=TimeoffType.objects.filter(status=1).values()
    if request.method == "POST":
        try:
            insert=TimeoffHeader.objects.create(subject=request.POST.get('subject'), description=request.POST.get('description'),
                                 time_off_type_id=request.POST.get('timeoff_type'), created_at=datetime.now(), updated_at=None, user_id=request.user.id)
            dates=request.POST.get('Dates')
            for date_string in dates.split(','):
                date_object = datetime.strptime(date_string, '%d/%m/%Y').date()
                TimeoffHeaderDateMapping.objects.create(timeoff_header_id=insert.id, date=date_object)
            messages.error(request, 'Submitted Successfull')
            return redirect('/timeoff/timeoff_list')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('/timeoff/add_timeoff')
    #pto and sick leaves counts
    pto_count=TimeoffHeaderDateMapping.objects.filter(timeoff_header_id__user_id=request.user.id,timeoff_header_id__time_off_type_id=1).count()
    sick_leave_count=TimeoffHeaderDateMapping.objects.filter(timeoff_header_id__user_id=request.user.id,timeoff_header_id__time_off_type_id=2).count()
    #applied timeoff
    mapped_timeoff=TimeoffHeader.objects.filter(user_id=request.user.id).values_list('id')
    all_applied_dates=list(TimeoffHeaderDateMapping.objects.filter(timeoff_header_id__in=mapped_timeoff).values_list('date',flat=True))
    formatted_dates = [date.strftime('%d/%m/%Y') for date in all_applied_dates]
    context={
        'timeoff_types':timeoff_types,'pto_count':pto_count,'sick_leave_count':sick_leave_count,'formatted_dates':formatted_dates
    }
    return render(request,'timeoff/add_timeoff.html',context)

@login_required
def timeoff_list(request):
    timeoff_header=TimeoffHeader.objects.filter(user_id=request.user.id).values('time_off_type_id','time_off_type_id__name','subject','id','description','created_at','updated_at')
    date_mapping=TimeoffHeaderDateMapping.objects.filter(timeoff_header_id__in=timeoff_header.values_list('id')).values()
    for i in timeoff_header:
        dates=[]
        for j in date_mapping:
            if i['id'] == j['timeoff_header_id']:
                d=j['date'].strftime('%d-%m-%Y')
                dates.append(d)
        i['dates']=",".join(dates)
    return render(request, 'timeoff/timeoff_list.html', {'timeoff_header':timeoff_header})

@login_required
def timeoff_delete(request,id):
    TimeoffHeader.objects.filter(user_id=request.user.id,id=id).delete()
    messages.success(request,'Deleted Successfully')
    return redirect('/timeoff/timeoff_list')

@login_required
def timeoff_edit(request,id):
    timeoff_header=TimeoffHeader.objects.get(user_id=request.user.id,id=id)
    date_mapping = TimeoffHeaderDateMapping.objects.filter(timeoff_header_id=id).values()
    dates = []
    for j in date_mapping:
        d = j['date'].strftime('%d-%m-%Y')
        dates.append(d)
    if request.method == "POST":
        timeoff_header.subject=request.POST.get('subject')
        timeoff_header.description=request.POST.get('description')
        timeoff_header.updated_at=datetime.now()
        timeoff_header.save()
        messages.success(request,'Updated Successfully')
        return redirect('/timeoff/timeoff_list')
    else:
        return render(request, 'timeoff/edit_timeoff.html', {'timeoff_header':timeoff_header,'dates':",".join(dates)})