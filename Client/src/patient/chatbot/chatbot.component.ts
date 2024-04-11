// src/patient/chatbot/chatbot.component.ts
import { Component } from '@angular/core';
import { ChatbotService } from '../services/chatbot.service';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.sass']
})
export class ChatbotComponent {
  symptoms: string = '';
  response: string = '';
  healthConditions: string = '';
  labReportPath: string = '';

  constructor(private chatbotService: ChatbotService) {}

  sendSymptoms() {
    this.chatbotService.analyzeSymptoms(this.symptoms).subscribe(
      (response) => {
        this.response = response.symptom_analysis;
      },
      (error) => {
        console.error('Error analyzing symptoms:', error);
      }
    );
  }

  sendHealthConditions() {
    this.chatbotService.analyzeHealthConditions(this.healthConditions).subscribe(
      (response) => {
        this.response = response.health_condition_analysis;
      },
      (error) => {
        console.error('Error analyzing health conditions:', error);
      }
    );
  }

  sendLabReport() {
    this.chatbotService.analyzeLabReport(this.labReportPath).subscribe(
      (response) => {
        this.response = response.lab_report_analysis;
      },
      (error) => {
        console.error('Error analyzing lab report:', error);
      }
    );
  }
}