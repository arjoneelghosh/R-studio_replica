A web-based forecasting application developed in Python that replicates the functionality of RStudio’s time-series forecasting tools. This system enables users to perform reliable forecasts using ARIMA and Prophet models, as used by business analysts and data professionals.

Features:
- Time-series forecasting using ARIMA (`pmdarima`) and Prophet (`prophet`)
- Automatic model selection based on AIC or RMSE
- Interactive forecast visualizations
- Support for CSV-based data uploads
- Export of forecasted results
- Modern frontend developed using React and Tailwind CSS
- Streamlit-based backend interface

Usage:
.Upload a time-series dataset (with date and metric columns).
.Select a forecast horizon and optional model parameters.
.The system fits both ARIMA and Prophet models.
.Outputs include forecast graphs, evaluation metrics, and downloadable results.

Dependencies:
Backend
.pandas
.pmdarima
.prophet
.matplotlib
.scikit-learn
.streamlit

Frontend:
.React
.Vite
.TailwindCSS
.Lucide-react

Deployment:
Frontend: Vercel, Netlify
Backend: Streamlit Community Cloud
