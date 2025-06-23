import { Component } from "@angular/core"
import { CommonModule } from "@angular/common"
import { HttpClientModule } from "@angular/common/http"
import { AudioPipelineComponent } from "./components/audio-pipeline/audio-pipeline"

@Component({
  selector: "app-root",
  standalone: true,
  imports: [CommonModule, HttpClientModule, AudioPipelineComponent],
  templateUrl: "./app.html",
  styleUrl: "./app.scss",
})
export class AppComponent {
  title = "Magic Mirror"
}
