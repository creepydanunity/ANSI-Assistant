
## Agreements and Decisions (2025-03-01)
- The team agreed to include the Analytics Dashboard in the July sprint.
- Dmitry confirmed that the UI for the Analytics Dashboard is ready.
- Ivan decided to work on the backend of the Analytics Dashboard, specifically exposing two endpoints: GET /api/v2/metrics/summary and GET /api/v2/metrics/daily.
- Ivan also decided to add basic JWT-based access control for the Analytics Dashboard.
- Ivan suggested using whisper.cpp locally for the voice command feature, using WebSocket to stream audio chunks and debounce inputs in ~10–15s windows, eliminating the need for external services.

## Open Questions (2025-03-01)
- The team needs to decide on the STT backend for the voice command feature. Ivan suggested Whisper, but no final decision was made.

## Agreements and Decisions (2025-06-01)
- Olga confirmed that the dashboard UI is still in progress with about 40% of the first layout completed.
- Dmitry clarified that the dashboard was still in design review last week, resolving Ivan's confusion.
- Ivan confirmed that he implemented /api/v2/metrics/summary and /metrics/daily for the backend API, which was previously agreed upon.
- Dmitry and Ivan agreed to align the backend API specifications later.
- Dmitry suggested using REST polling for voice feedback, with the frontend sending recorded audio every 5 seconds.

## Open Questions (2025-06-01)
- There is a discrepancy between the backend API spec and what Ivan implemented. This needs to be resolved.
- Ivan and Dmitry have different understandings of the voice feedback mechanism. Ivan thought they were using local Whisper over WebSocket, while Dmitry suggested REST polling. This needs to be clarified.
- Olga hasn't wired up MediaRecorder yet because she was assuming a real-time stream. This needs to be addressed based on the decision about the voice feedback mechanism.

## Agreements and Decisions (2025-03-01)
- The team decided to include the Analytics Dashboard in the July sprint, with the backend to be hooked up.
- Ivan agreed to expose two endpoints: GET /api/v2/metrics/summary and GET /api/v2/metrics/daily, and to add basic JWT-based access control.
- The team discussed the voice command feature and Ivan suggested using whisper.cpp locally with WebSocket to stream audio chunks and debounce inputs in ~10–15s windows.

## Open Questions (2025-03-01)
- The team needs to make a decision on the Speech-To-Text (STT) backend for the voice command feature. Whisper was suggested but no final decision was made.

## Agreements and Decisions (2025-06-01)
- Olga confirmed that the UI for the dashboard is 40% complete.
- Ivan implemented /api/v2/metrics/summary and /metrics/daily as per previous agreement.
- Dmitry suggested aligning the backend API specifications later.
- Ivan reminded the team about the decision to use local Whisper over WebSocket for voice.
- Dmitry proposed using REST polling for voice, with the frontend sending recorded audio every 5 seconds.
- Ivan and Olga expressed the need for real-time voice feedback.

## Open Questions (2025-06-01)
- There is a discrepancy between the backend API specifications in the spec and what Ivan implemented. This needs to be resolved.
- The method for implementing voice feedback is still under discussion. The team needs to decide between REST polling and real-time streaming.
- Olga needs to wire up MediaRecorder for real-time streaming, pending the team's decision on the voice feedback method.

## Agreements and Decisions (2025-03-01)
- The team decided to include the Analytics Dashboard in the July sprint.
- Ivan will expose two endpoints: GET /api/v2/metrics/summary and GET /api/v2/metrics/daily for the Analytics Dashboard.
- Ivan will add basic JWT-based access control for the Analytics Dashboard.
- The team agreed to use whisper.cpp locally for the voice command feature, using WebSocket to stream audio chunks and debounce inputs in ~10–15s windows.

## In Progress / Claimed Tasks (2025-03-01)
- Ivan claimed the task of exposing two endpoints and adding basic JWT-based access control for the Analytics Dashboard.
- The team is working on the voice command feature, with a decision made to use whisper.cpp locally.

## Open Questions (2025-03-01)
- The team is undecided on the Speech-To-Text (STT) backend for the voice command feature.

## Agreements and Decisions (2025-06-01)
- The team agreed to align the backend API specifications later.
- The team decided to use local Whisper over WebSocket for voice interaction.
- The team agreed that frontend should send recorded audio every 5 seconds.

## In Progress / Claimed Tasks (2025-06-01)
- Olga is working on the UI for the dashboard, which is about 40% complete.
- Ivan has implemented /api/v2/metrics/summary and /metrics/daily as per previous agreement.
- Olga needs to wire up MediaRecorder for real-time stream.

## Open Questions (2025-06-01)
- There is a discrepancy between the backend API specifications in the spec and what Ivan implemented. This needs to be resolved.
- There is a discussion about whether to use REST polling or real-time stream for voice interaction. The team needs to finalize this.
