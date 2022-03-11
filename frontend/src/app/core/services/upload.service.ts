import { DOCUMENT } from '@angular/common';
import { Inject, Injectable, Renderer2, RendererFactory2 } from '@angular/core';

type InputAcceptOption = 'image/*'
  | '.jpg'
  | '.jpeg'
  | '.png';

@Injectable({
  providedIn: 'root'
})
export class UploadService {

  private renderer: Renderer2;

  constructor(
    @Inject(DOCUMENT) private document: Document,
    rendererFactory: RendererFactory2
  ) {
    this.renderer = rendererFactory.createRenderer(null, null);
  }

  async upload(accept?: InputAcceptOption | InputAcceptOption[], multiple = false) {
    return new Promise<string[] | null>((resolve, reject) => {
      const input = this.createInput(accept)
      this.renderer.appendChild(this.document.body, input)
      input.onchange = () => {
        try {
          resolve(this.handleFileChange(input, multiple))
        } catch (error) {
          reject(error)
        } finally {
          this.renderer.removeChild(this.document.body, input)
        }
      }
      input.click()
    })
  }

  private async handleFileChange(input: HTMLInputElement, multiple: boolean): Promise<string[] | null> {
    return new Promise((resolve, reject) => {
      if (input.files && input.files.length > 0) {
        let files: File[] = Array.from(input.files)
        const filesBase64: string[] = []
        files.forEach(async file => {
          try {
            const fileString = await this.readFileAsync(file)
            filesBase64.push(fileString)
          } catch (error) {
            reject(error)
          }
        })
        resolve(filesBase64)
      }
      resolve(null)
    })
  }

  private readFileAsync(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => {
        const base64 = (reader.result as string).split(',')[1]
        resolve(base64)
      }
      reader.onerror = reject
    })
  }

  private createInput(accept?: InputAcceptOption | InputAcceptOption[]): HTMLInputElement {
    const input = this.renderer.createElement('input')
    this.renderer.setAttribute(input, 'type', 'file')
    this.renderer.addClass(input, 'd-none')
    if (accept) {
      if (Array.isArray(accept)) {
        this.renderer.setAttribute(input, 'accept', accept.join(','))
      } else {
        this.renderer.setAttribute(input, 'accept', accept)
      }
    }
    return input
  }
}
