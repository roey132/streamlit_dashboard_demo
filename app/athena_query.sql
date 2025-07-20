SELECT
  time,
  latitude,
  longitude,
  depth,
  mag,
  magType,
  place,
  type,
  status,
  tsunami,
  sig,
  net,
  id
FROM
  batch_data_demo.earthquakes
ORDER BY
  time DESC
