import { Component, inject, type OnDestroy } from "@angular/core"
import { CommonModule } from "@angular/common"
import { HttpClient } from "@angular/common/http"
import { FormsModule } from "@angular/forms"
import { interval, type Subscription } from "rxjs"
import { environment } from "C:\Users\Devan\Desktop\audio_pipeline_project\frontend\src\environments\environments.ts"

interface PipelineResponse {
  success: boolean
  user_transcript: string
  claude_response: string
  tts_file: string
  duration_recorded: number
  message: string
  stream_active?: boolean
}

interface ProgressState {
  current_step: number
  status: string
  transcript: string
  claude_response: string
  error: string | null
  stream_active: boolean
}

@Component({
  selector: "app-audio-pipeline",
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: "./audio-pipeline.html",
  styleUrl: "./audio-pipeline.scss",
})
export class AudioPipelineComponent implements OnDestroy {
  private http = inject(HttpClient)
  private progressSubscription?: Subscription

  duration = 5
  isProcessing = false
  isRecording = false
  currentStep = 0
  result: PipelineResponse | null = null
  error: string | null = null
  streamActive = false

  readonly API_URL = environment.apiUrl

  getButtonText(): string {
    if (this.isRecording) return "Recording..."
    if (this.isProcessing) return "AI Processing..."
    return "Start Conversation"
  }

  async startRecording() {
    if (this.isProcessing) return

    this.isProcessing = true
    this.isRecording = true
    this.currentStep = 0
    this.result = null
    this.error = null
    this.streamActive = false

    this.startProgressPolling()

    try {
      const response = await this.http
        .post<PipelineResponse>(`${this.API_URL}/record_and_speak`, {
          duration: this.duration,
        })
        .toPromise()

      this.result = response!
      this.isProcessing = false
      this.streamActive = response?.stream_active || false
    } catch (err: any) {
      this.error = err.error?.error || "AI conversation failed"
      this.isProcessing = false
      this.isRecording = false
      this.currentStep = 0
      this.streamActive = false
    } finally {
      this.stopProgressPolling()
    }
  }

  private startProgressPolling() {
    this.progressSubscription = interval(500).subscribe(() => {
      this.http.get<ProgressState>(`${this.API_URL}/progress`).subscribe({
        next: (progress) => {
          this.currentStep = progress.current_step
          this.isRecording = progress.status === "recording"

          // Update result with real-time data
          if (progress.transcript || progress.claude_response) {
            this.result = {
              ...this.result,
              user_transcript: progress.transcript,
              claude_response: progress.claude_response,
            } as PipelineResponse
          }

          if (progress.error) {
            this.error = progress.error
            this.isProcessing = false
            this.isRecording = false
          }

          this.streamActive = progress.stream_active
        },
        error: (err) => console.warn("Progress polling error:", err),
      })
    })
  }

  private stopProgressPolling() {
    if (this.progressSubscription) {
      this.progressSubscription.unsubscribe()
      this.progressSubscription = undefined
    }
  }

  async startStream() {
    try {
      const response = await this.http.post(`${this.API_URL}/stream/start`, {}).toPromise()
      this.streamActive = true
      console.log("Stream started:", response)
    } catch (err) {
      console.error("Failed to start stream:", err)
    }
  }

  async stopStream() {
    try {
      const response = await this.http.post(`${this.API_URL}/stream/stop`, {}).toPromise()
      this.streamActive = false
      console.log("Stream stopped:", response)
    } catch (err) {
      console.error("Failed to stop stream:", err)
    }
  }

  clearError() {
    this.error = null
    this.currentStep = 0
    this.streamActive = false
  }

  ngOnDestroy() {
    this.stopProgressPolling()
  }
}
