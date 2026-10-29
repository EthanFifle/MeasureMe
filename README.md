# MeasureMe

Body-measurement extraction service used by [Techpack](https://github.com/EthanFifle/techpack). Accepts SMPL body-shape parameters and returns measurements through a Flask API. Research prototype from 2024.

`app.py` exposes `POST /betas`, which takes `gender` (male, female or neutral) and `betas` (SMPL shape parameters as a JSON string) and returns the measurements as JSON. `techpack.py` connects the measurement code to that endpoint.

Built on [SMPL-Anthropometry](https://github.com/DavidBoja/SMPL-Anthropometry) by David Bojanić; see `LICENSE`.
