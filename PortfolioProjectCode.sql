/*--Looking a Total Cases vs Population, this shows what percentage of the population got COVID by continents*/
SELECT location, MAX(total_cases) AS Cases, population, ROUND((1.0*total_cases/population*100),2) AS InfectedPercentage
FROM CovidDeaths
WHERE continent IS NULL AND population IS NOT NULL AND total_cases IS NOT NULL
GROUP BY location
ORDER BY InfectedPercentage DESC


/*--Looking a Total Cases vs Population, this shows what percentage of the population got COVID by country*/
SELECT location, MAX(total_cases) AS Cases, population, ROUND((1.0*total_cases/population*100),2) AS InfectedPercentage
FROM CovidDeaths
WHERE population IS NOT NULL AND total_cases IS NOT NULL
GROUP BY location
ORDER BY InfectedPercentage DESC


/*--Looking a Total Cases vs Population, this shows what percentage of the population got COVID in the US only*/
SELECT location, MAX(total_cases) AS Cases, population, ROUND((1.0*total_cases/population*100),2) AS InfectedPercentage
FROM CovidDeaths
WHERE location LIKE '%states%'


/*--Looking at Total Deaths vs Total Cases by continents*/
SELECT location,  MAX(total_deaths) AS Deaths, MAX(total_cases) AS Cases, ROUND(1.0*MAX(total_deaths)/MAX(total_cases)*100,2) AS MortalityRate
FROM CovidDeaths
WHERE total_deaths IS NOT NULL AND total_cases IS NOT NULL AND continent IS NULL
GROUP BY location
ORDER BY MortalityRate DESC


/*--Looking at Total Deaths vs Total Cases by country*/
SELECT location,  MAX(total_deaths) AS Deaths, MAX(total_cases) AS Cases, ROUND(1.0*MAX(total_deaths)/MAX(total_cases)*100,2) AS MortalityRate
FROM CovidDeaths
WHERE total_deaths IS NOT NULL AND total_cases IS NOT NULL AND continent IS NOT NULL
GROUP BY location
ORDER BY MortalityRate DESC



/*--Looking at Total Deaths vs Total Cases in the US only*/
SELECT location, MAX(total_deaths) AS Deaths, MAX(total_cases) AS Cases, ROUND(1.0*MAX(total_deaths)/MAX(total_cases)*100,2) AS MortalityRate
FROM CovidDeaths
WHERE location LIKE '%states%'


/*--Looking at Total Population vs Vaccinations with rolling count of rolling vaccinations*/
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingVaccinationCount
FROM CovidDeaths dea
JOIN CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL AND new_vaccinations IS NOT NULL
ORDER BY 2,3 ASC


/*
--Using a temp TABLE*/
DROP TABLE IF EXISTS PercentPopulationVaccinated
CREATE TABLE PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
population numeric,
new_vaccinations numeric,
RollingVaccinationCount NUMERIC
)

INSERT INTO PercentPopulationVaccinated
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingVaccinationCount
FROM CovidDeaths dea
JOIN CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL AND new_vaccinations IS NOT NULL
ORDER BY 2,3 ASC

SELECT * FROM PercentPopulationVaccinated



/*--Creating view to store data for later visualizations*/
Create VIEW PercentPopulationVaccinated AS
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingVaccinationCount
FROM CovidDeaths dea
JOIN CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL AND new_vaccinations IS NOT NULL
ORDER BY 2,3 ASC
