
import datetime
from django.apps import apps as django_apps
from edc_appointment.models import Appointment

from ..models import AppointmentStatus


class AppointmentHelper:
    
    child_appointment_model = 'flourish_child.appointment'
    

    @staticmethod
    def child_appointment_cls():
        return django_apps.get_model(AppointmentHelper.child_appointment_model)

    @staticmethod
    def change_color(subject_identifier, visit_code, color, appt_date):

        if subject_identifier and visit_code and color:

            try:

                appt = AppointmentStatus.objects.get(
                    subject_identifier=subject_identifier,
                    visit_code=visit_code,
                    appt_date=datetime.datetime.fromisoformat(appt_date).date()
                )

            except AppointmentStatus.DoesNotExist:

                AppointmentStatus.objects.create(
                    subject_identifier=subject_identifier,
                    visit_code=visit_code,
                    color=color,
                    appt_date=datetime.datetime.fromisoformat(appt_date).date()
                )

            else:
                appt.color = color
                appt.save()
                
    @classmethod           
    def all_search_appointments(cls, subject_identifier, type):
        
        results = []
        
        if subject_identifier:
        
            if type == 'caregiver':
                caregiver_appointments = Appointment.objects.filter(
                    subject_identifier__icontains=subject_identifier)
                results.extend(caregiver_appointments)
                
            elif type == 'children':
                children_appointments = AppointmentHelper.child_appointment_cls.objects.filter(
                    subject_identifier__icontains=subject_identifier)
                results.extend(children_appointments)
                
            else:
                
                caregiver_appointments = Appointment.objects.filter(
                    subject_identifier__icontains=subject_identifier)
                
                children_appointments = AppointmentHelper.child_appointment_cls.objects.filter(
                    subject_identifier__icontains=subject_identifier)

                results.extend(caregiver_appointments)
                results.extend(children_appointments)
        
        return results
