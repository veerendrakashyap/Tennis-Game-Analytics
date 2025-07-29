-- =======================================
-- 🎾 TENNIS DATA - SQL SCHEMA + QUERIES
-- Created by Veerendra Kashyap
-- =======================================

-- 1. Create and Select Database
CREATE DATABASE tennis_data;
USE tennis_data;

-- ========================
-- 2. TABLE CREATION
-- ========================

-- 2.1 Categories Table
CREATE TABLE categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- 2.2 Competitions Table
CREATE TABLE competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50),
    type VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    category_id VARCHAR(50),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- 2.3 Complexes Table
CREATE TABLE complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);

-- 2.4 Venues Table
CREATE TABLE venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    complex_id VARCHAR(50),
    FOREIGN KEY (complex_id) REFERENCES complexes(complex_id)
);

-- 2.5 Competitors Table
CREATE TABLE competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    abbreviation VARCHAR(10) NOT NULL
);

-- 2.6 Competitor Rankings Table
CREATE TABLE competitor_rankings (
    rank_id INT PRIMARY KEY AUTO_INCREMENT,
    `rank` INT NOT NULL,
    movement INT NOT NULL,
    points INT NOT NULL,
    competitions_played INT NOT NULL,
    competitor_id VARCHAR(50),
    FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id)
);

-- ========================
-- 3. BASIC CHECK QUERIES
-- ========================

-- View all competitors
SELECT * FROM competitors; 

-- View all rankings
SELECT * FROM competitor_rankings;

-- Join both tables
SELECT c.name, r.rank, r.points, r.movement
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id;

-- ==============================
-- 4. COMPETITIONS & CATEGORIES
-- ==============================

-- 4.1 List all competitions with category name
SELECT comp.competition_name, cat.category_name
FROM competitions comp
JOIN categories cat ON comp.category_id = cat.category_id;

-- 4.2 Count competitions per category
SELECT cat.category_name, COUNT(*) AS total_competitions
FROM competitions comp
JOIN categories cat ON comp.category_id = cat.category_id
GROUP BY cat.category_name;

-- 4.3 All doubles competitions
SELECT * FROM competitions WHERE type = 'doubles';

-- 4.4 Parent and sub-competitions
SELECT parent.competition_name AS Parent, child.competition_name AS Sub_Competition
FROM competitions child
JOIN competitions parent ON child.parent_id = parent.competition_id;

-- 4.5 Type distribution by category
SELECT cat.category_name, comp.type, COUNT(*) AS total
FROM competitions comp
JOIN categories cat ON comp.category_id = cat.category_id
GROUP BY cat.category_name, comp.type;

-- 4.6 Top-level competitions (no parent)
SELECT * FROM competitions WHERE parent_id IS NULL;

-- ========================
-- 5. VENUES & COMPLEXES
-- ========================

-- 5.1 Venues with complex name
SELECT v.venue_name, c.complex_name
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id;

-- 5.2 Count venues per complex
SELECT c.complex_name, COUNT(*) AS total_venues
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id
GROUP BY c.complex_name;

-- 5.3 Venues in Chile
SELECT * FROM venues WHERE country_name = 'Chile';

-- 5.4 Venue timezones
SELECT venue_name, timezone FROM venues;

-- 5.5 Complexes with more than 1 venue
SELECT complex_id, COUNT(*) AS venue_count
FROM venues
GROUP BY complex_id
HAVING COUNT(*) > 1;

-- 5.6 Venue count per country
SELECT country_name, COUNT(*) AS total_venues
FROM venues
GROUP BY country_name;

-- 5.7 Venues for a specific complex (e.g., Nacional)
SELECT * FROM venues WHERE complex_id = 'sr:complex:705';

-- ========================
-- 6. COMPETITOR RANKINGS
-- ========================

-- 6.1 Competitor name with rank and points
SELECT c.name, r.rank, r.points
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id;

-- 6.2 Top 5 ranked competitors
SELECT c.name, r.rank, r.points
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
ORDER BY r.rank ASC
LIMIT 5;

-- 6.3 Competitors with no rank movement
SELECT c.name, r.rank, r.movement
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
WHERE r.movement = 0;

-- 6.4 Competitor count per country
SELECT country, COUNT(*) AS total_competitors
FROM competitors
GROUP BY country;

-- 6.5 Competitor with highest points
SELECT c.name, r.points
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
ORDER BY r.points DESC
LIMIT 1;



  
  
  
  
  
