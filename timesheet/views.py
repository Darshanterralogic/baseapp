from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from timeoff.models import *
from datetime import datetime
from django.contrib import messages

# Create your views here.
@login_required
def add_timesheet(request):
    # applied timeoff exclude WFH
    mapped_timeoff = TimeoffHeader.objects.filter(user_id=request.user.id).exclude(time_off_type_id=3).values_list('id')
    all_applied_dates = list(TimeoffHeaderDateMapping.objects.filter(timeoff_header_id__in=mapped_timeoff).values_list('date', flat=True))
    formatted_dates = [date.strftime('%d/%m/%Y') for date in all_applied_dates]
    if request.method == "POST":
        try:
            s=request.POST.get
            date_object = datetime.strptime(s('date'), '%d/%m/%Y').date()
            TimeSheetHeader.objects.create(task=s('task'), task_date=date_object, description=s('description'), created_at=datetime.now(),user_id=request.user.id)
            messages.error(request, 'Submitted Successfull')
            return redirect('/timesheet/timesheet_list')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('/timesheet/add_timesheet')
    context={
        'formatted_dates':formatted_dates
    }
    return render(request,'timesheet/add_timesheet.html',context)

@login_required
def timesheet_list(request):
    time_sheet=TimeSheetHeader.objects.filter(user_id=request.user.id).values()
    return render(request, 'timesheet/timesheet_list.html',{'time_sheet':time_sheet})

@login_required
def timesheet_delete(request,id):
    TimeSheetHeader.objects.filter(id=id,user_id=request.user.id).delete()
    messages.success(request,'Deleted Successfully')
    return redirect('/timesheet/timesheet_list')

@login_required
def timesheet_edit(request,id):
    timesheet_header=TimeSheetHeader.objects.get(user_id=request.user.id, id=id)
    if request.method == "POST":
        timesheet_header.task=request.POST.get('task')
        timesheet_header.description=request.POST.get('description')
        timesheet_header.updated_at=datetime.now()
        timesheet_header.save()
        messages.success(request,'Updated Successfully')
        return redirect('/timesheet/timesheet_list')
    else:
        return render(request, 'timesheet/edit_timesheet.html',{'timesheet_header':timesheet_header})