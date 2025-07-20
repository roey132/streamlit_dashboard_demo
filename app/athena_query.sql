SELECT
id,
magnitude,
place,
time_utc,
latitude,
longitude,
depth_km,
status,
type,
tsunami,
alert,
year,
month,
day

FROM
  batch_data_demo.earthquakes
ORDER BY
  time_utc DESC
