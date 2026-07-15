SELECT
    System.Timestamp() AS WindowEndTime,
    sensorId,
    AVG(temperature) AS AvgTemp,
    SUM(energyConsumption) AS TotalEnergy,
    COUNT(*) AS ReadingCount
INTO
    [PowerBIOutput]  -- <--- Make sure this matches your Output Alias!
FROM
    [FactoryStream]
GROUP BY
    sensorId,
    TumblingWindow(second, 10)
