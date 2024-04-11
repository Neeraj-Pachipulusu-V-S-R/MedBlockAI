// src/patient/services/chatbot.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {
  private apiUrl = '/api/chatbot/';

  constructor(private http: HttpClient) {}

  analyzeSymptoms(symptoms: string): Observable<any> {
    return this.http.post(this.apiUrl, { symptoms });
  }

  analyzeHealthConditions(healthConditions: string): Observable<any> {
    return this.http.post(this.apiUrl, { health_conditions: healthConditions });
  }

  analyzeLabReport(labReportPath: string): Observable<any> {
    return this.http.post(this.apiUrl, { lab_report_path: labReportPath });
  }
}