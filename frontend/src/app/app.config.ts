import { type ApplicationConfig, importProvidersFrom } from "@angular/core"
import { provideRouter } from "@angular/router"
import { HttpClientModule } from "@angular/common/http"

export const appConfig: ApplicationConfig = {
  providers: [provideRouter([]), importProvidersFrom(HttpClientModule)],
}
