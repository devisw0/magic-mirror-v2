import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AudioPipeline } from './audio-pipeline';

describe('AudioPipeline', () => {
  let component: AudioPipeline;
  let fixture: ComponentFixture<AudioPipeline>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AudioPipeline]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AudioPipeline);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
