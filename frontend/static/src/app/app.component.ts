import { Component } from '@angular/core';
import { FileUploader } from 'ng2-file-upload/ng2-file-upload';

const URL = '/api/predict';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app';
  imageData: string = "";
  predictionScores: any = [];

  public uploader: FileUploader = new FileUploader({url: URL, itemAlias: 'image'});
  
  constructor() { }

  ngOnInit() {
    this.uploader.onAfterAddingFile = (file) => { 
      this.predictionScores = [];
      file.withCredentials = false; 
      const fileReader: FileReader = new FileReader();
      fileReader.onload = e => this.imageData = fileReader.result;
      fileReader.readAsDataURL(file._file); 
    };
    this.uploader.onCompleteItem = (item: any, response: any, status: any, headers: any) => {
      console.log('ImageUpload:uploaded:', item, status, response);  
      this.predictionScores = JSON.parse(response);
     };
 	}
  
}
