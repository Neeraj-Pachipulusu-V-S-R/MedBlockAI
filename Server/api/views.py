from dataclasses import dataclass
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Appointment, Doctor, Patient
from .serializers import AppointmentSerializer, DoctorSerializer, PatientSerializer

# Create your views here.


class DoctorView(APIView):
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            doctor = Doctor.objects.filter(docID=id)
            serializer = DoctorSerializer(doctor,many = True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response({"status": "success", "data": serializer.data}, status.HTTP_200_OK)

    def delete(self, request, id=None):
        doctor = Doctor.objects.filter(docID=id)
        doctor.delete()
        
        return Response({"status": "success", "data": True})


class PatientView(APIView):
    def post(self, request):
        serializer = PatientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AppointmentView(APIView):
    def post(self, request):

        doctor = Doctor.objects.get(docID=request.data.get('docID'))
        patient = Patient.objects.get(patID=request.data.get('patID'))

        request.data._mutable = True
        request.data['docName'] = doctor.fName + ' ' + doctor.lName
        request.data['patName'] = patient.patName
        request.data._mutable = False

        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response({"status": "success", "data": serializer.data}, status.HTTP_200_OK)

    def put(self, request, id):
        appointment = Appointment.objects.get(id=id)
        appointment.status = True
        appointment.save()
        return Response({"status": "success", "data": appointment.status}, status.HTTP_200_OK)


class ChatbotView(APIView):
    def post(self, request):
        data = request.data
        symptoms = data.get('symptoms', '')
        health_conditions = data.get('health_conditions', '')
        lab_report_path = data.get('lab_report_path', '')

        response_data = {}

        # Analyze symptoms
        if symptoms:
            response_data['symptom_analysis'] = generate_gemini_content(f"A user reports the following symptoms: {symptoms}. What general advice should be given?")

        # Analyze health conditions
        if health_conditions:
            response_data['health_condition_analysis'] = generate_gemini_content(f"A user has these health conditions: {health_conditions}. How should this affect their care for the symptoms mentioned earlier?")

        # Analyze lab report
        if lab_report_path:
            lab_report_text = extract_text_from_pdf(lab_report_path)
            if lab_report_text:
                response_data['lab_report_analysis'] = generate_gemini_content(f"The following text is extracted from a user's lab report: {lab_report_text[:100000]}. What insights can be drawn?")
            else:
                response_data['lab_report_analysis'] = "Unable to extract text from the lab report or file is empty."

        return Response(response_data)



@api_view(['GET'])
def getAppointmentDoc(self, id):

    appointment = Appointment.objects.filter(docID=id)
    serializer = AppointmentSerializer(appointment, many=True)
    return Response({"status": "success", "data": serializer.data}, status.HTTP_200_OK)


@api_view(['GET'])
def getAppointmentPat(self, id):

    appointment = Appointment.objects.filter(patID=id)
    serializer = AppointmentSerializer(appointment, many=True)
    return Response({"status": "success", "data": serializer.data}, status.HTTP_200_OK)


@api_view(['GET'])
def getCount(self):
    doctorCount = Doctor.objects.all().count()
    patientCount = Patient.objects.all().count()
    return Response({"status": "success", "docCount": doctorCount, "patCount": patientCount}, status.HTTP_200_OK)


@api_view(['GET'])
def clear(self):
    Doctor.objects.all().delete()
    Appointment.objects.alias().delete()
    Patient.objects.alias().delete()

    return Response({"status": "success"}, status.HTTP_200_OK)