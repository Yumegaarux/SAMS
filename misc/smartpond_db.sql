-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 02, 2025 at 09:13 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smartpond_dbs`
--

-- --------------------------------------------------------

--
-- Table structure for table `activity_archive`
--

CREATE TABLE `activity_archive` (
  `AAID` int(11) NOT NULL,
  `Date` date NOT NULL,
  `Activity` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `batch_bridge`
--

CREATE TABLE `batch_bridge` (
  `BBID` int(11) NOT NULL,
  `fishID` int(11) NOT NULL,
  `FBID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `fish`
--

CREATE TABLE `fish` (
  `fishID` int(11) NOT NULL,
  `fish_name` varchar(30) NOT NULL,
  `minSalinityTol` float NOT NULL,
  `maxSalinityTol` float NOT NULL,
  `minpHTol` float NOT NULL,
  `maxpHTol` float NOT NULL,
  `feedingFrequencyReq` int(11) NOT NULL,
  `recHarvestPeriod` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fish`
--

INSERT INTO `fish` (`fishID`, `fish_name`, `minSalinityTol`, `maxSalinityTol`, `minpHTol`, `maxpHTol`, `feedingFrequencyReq`, `recHarvestPeriod`) VALUES
(1, 'a', 1, 1, 1, 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `fish_batch`
--

CREATE TABLE `fish_batch` (
  `FBID` int(11) NOT NULL,
  `fishID` int(11) NOT NULL,
  `minSalinity` float NOT NULL,
  `maxSalinity` float NOT NULL,
  `minpH` float NOT NULL,
  `maxpH` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fish_batch`
--

INSERT INTO `fish_batch` (`FBID`, `fishID`, `minSalinity`, `maxSalinity`, `minpH`, `maxpH`) VALUES
(1, 1, 1, 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `fish_tank`
--

CREATE TABLE `fish_tank` (
  `tankID` int(11) NOT NULL,
  `FBID` int(11) NOT NULL,
  `plantID` int(11) NOT NULL,
  `minSalinity` float NOT NULL,
  `maxSalinity` float NOT NULL,
  `minpH` float NOT NULL,
  `maxpH` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fish_tank`
--

INSERT INTO `fish_tank` (`tankID`, `FBID`, `plantID`, `minSalinity`, `maxSalinity`, `minpH`, `maxpH`) VALUES
(1, 1, 1, 1, 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `notifID` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `alert` varchar(30) NOT NULL,
  `suggestion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plant`
--

CREATE TABLE `plant` (
  `plantID` int(11) NOT NULL,
  `plant_name` varchar(30) NOT NULL,
  `minSalinityTol` float NOT NULL,
  `maxSalinityTol` float NOT NULL,
  `minpHTol` float NOT NULL,
  `maxpHTol` float NOT NULL,
  `wateringFrequencyReq` int(11) NOT NULL,
  `recHarvestPeriod` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `plant`
--

INSERT INTO `plant` (`plantID`, `plant_name`, `minSalinityTol`, `maxSalinityTol`, `minpHTol`, `maxpHTol`, `wateringFrequencyReq`, `recHarvestPeriod`) VALUES
(1, 'a', 1, 1, 1, 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `record_archive`
--

CREATE TABLE `record_archive` (
  `RAID` int(11) NOT NULL,
  `date` date NOT NULL,
  `avgpHlevel` float NOT NULL,
  `avgSalinity` float NOT NULL,
  `Remarks` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sensor`
--

CREATE TABLE `sensor` (
  `sensorID` int(11) NOT NULL,
  `sensorName` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sensor`
--

INSERT INTO `sensor` (`sensorID`, `sensorName`) VALUES
(1, 'pH Sensor'),
(2, 'Salinity');

-- --------------------------------------------------------

--
-- Table structure for table `sensor_logs`
--

CREATE TABLE `sensor_logs` (
  `SensorLogID` int(11) NOT NULL,
  `sensorID` int(11) NOT NULL,
  `tankID` int(11) NOT NULL,
  `data` float NOT NULL,
  `datetime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sensor_logs`
--

INSERT INTO `sensor_logs` (`SensorLogID`, `sensorID`, `tankID`, `data`, `datetime`) VALUES
(1, 1, 1, 7.1036, '2025-07-02 11:09:16'),
(2, 2, 1, 0.0008, '2025-07-02 11:09:16'),
(3, 1, 1, 7.11692, '2025-07-02 11:10:16'),
(4, 2, 1, 0.000769231, '2025-07-02 11:10:16'),
(5, 1, 1, 7.12269, '2025-07-02 11:11:16'),
(6, 2, 1, 0.000384615, '2025-07-02 11:11:16'),
(7, 1, 1, 7.11875, '2025-07-02 11:12:16'),
(8, 2, 1, 0, '2025-07-02 11:12:16'),
(9, 1, 1, 7.1225, '2025-07-02 11:13:16'),
(10, 2, 1, 0, '2025-07-02 11:13:16'),
(11, 1, 1, 7.14923, '2025-07-02 11:14:16'),
(12, 2, 1, 0.000384615, '2025-07-02 11:14:16'),
(13, 1, 1, 7.16583, '2025-07-02 11:15:16'),
(14, 2, 1, 0.000416667, '2025-07-02 11:15:16'),
(15, 1, 1, 7.13583, '2025-07-02 11:17:08'),
(16, 2, 1, 0.000833333, '2025-07-02 11:17:08'),
(17, 1, 1, 7.05115, '2025-07-02 11:18:08'),
(18, 2, 1, 0.00884615, '2025-07-02 11:18:08'),
(19, 1, 1, 7.13346, '2025-07-02 11:19:08'),
(20, 2, 1, 0.03, '2025-07-02 11:19:08'),
(21, 1, 1, 7.09667, '2025-07-02 11:20:08'),
(22, 2, 1, 0.03, '2025-07-02 11:20:08'),
(23, 1, 1, 7.09545, '2025-07-02 11:21:08'),
(24, 2, 1, 0.03, '2025-07-02 11:21:08'),
(25, 1, 1, 7.13667, '2025-07-02 11:22:08'),
(26, 2, 1, 0.03, '2025-07-02 11:22:08'),
(27, 1, 1, 7.15174, '2025-07-02 11:24:08'),
(28, 2, 1, 0.0369565, '2025-07-02 11:24:08'),
(29, 1, 1, 7.11154, '2025-07-02 11:25:08'),
(30, 2, 1, 0.04, '2025-07-02 11:25:08'),
(31, 1, 1, 7.12261, '2025-07-02 11:26:08'),
(32, 2, 1, 0.04, '2025-07-02 11:26:08'),
(33, 1, 1, 7.13038, '2025-07-02 11:27:08'),
(34, 2, 1, 0.04, '2025-07-02 11:27:08'),
(35, 1, 1, 7.09391, '2025-07-02 11:28:09'),
(36, 2, 1, 0.04, '2025-07-02 11:28:09'),
(37, 1, 1, 7.13458, '2025-07-02 11:29:09'),
(38, 2, 1, 0.04, '2025-07-02 11:29:09'),
(39, 1, 1, 7.1424, '2025-07-02 11:30:09'),
(40, 2, 1, 0.04, '2025-07-02 11:30:09'),
(41, 1, 1, 7.01833, '2025-07-02 11:31:09'),
(42, 2, 1, 0.04, '2025-07-02 11:31:09'),
(43, 1, 1, 7.10261, '2025-07-02 11:32:09'),
(44, 2, 1, 0.04, '2025-07-02 11:32:09'),
(45, 1, 1, 7.07042, '2025-07-02 11:33:09'),
(46, 2, 1, 0.04, '2025-07-02 11:33:09'),
(47, 1, 1, 7.153, '2025-07-02 11:34:09'),
(48, 2, 1, 0.04, '2025-07-02 11:34:09'),
(49, 1, 1, 7.18, '2025-07-02 11:35:09'),
(50, 2, 1, 0.04, '2025-07-02 11:35:09'),
(51, 1, 1, 7.00593, '2025-07-02 11:36:09'),
(52, 2, 1, 0.04, '2025-07-02 11:36:09'),
(53, 1, 1, 7.168, '2025-07-02 11:37:09'),
(54, 2, 1, 0.04, '2025-07-02 11:37:09'),
(55, 1, 1, 7.04423, '2025-07-02 11:38:09'),
(56, 2, 1, 0.04, '2025-07-02 11:38:09'),
(57, 1, 1, 7.29917, '2025-07-02 11:39:09'),
(58, 2, 1, 0.04, '2025-07-02 11:39:09'),
(59, 1, 1, 7.19111, '2025-07-02 11:40:09'),
(60, 2, 1, 0.04, '2025-07-02 11:40:09'),
(61, 1, 1, 7.124, '2025-07-02 11:41:09'),
(62, 2, 1, 0.04, '2025-07-02 11:41:09'),
(63, 1, 1, 7.09, '2025-07-02 11:42:47');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userID` int(11) NOT NULL,
  `lname` varchar(30) NOT NULL,
  `fname` varchar(30) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `email` varchar(60) NOT NULL,
  `contact_number` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userID`, `lname`, `fname`, `username`, `password`, `email`, `contact_number`) VALUES
(1, 'a', 'a', 'a', 'a', 'a', '1');

-- --------------------------------------------------------

--
-- Table structure for table `user_tank`
--

CREATE TABLE `user_tank` (
  `UTID` int(11) NOT NULL,
  `userID` int(11) NOT NULL,
  `tankID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_tank`
--

INSERT INTO `user_tank` (`UTID`, `userID`, `tankID`) VALUES
(1, 1, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_archive`
--
ALTER TABLE `activity_archive`
  ADD PRIMARY KEY (`AAID`);

--
-- Indexes for table `batch_bridge`
--
ALTER TABLE `batch_bridge`
  ADD PRIMARY KEY (`BBID`),
  ADD KEY `fishID` (`fishID`),
  ADD KEY `FBID` (`FBID`);

--
-- Indexes for table `fish`
--
ALTER TABLE `fish`
  ADD PRIMARY KEY (`fishID`);

--
-- Indexes for table `fish_batch`
--
ALTER TABLE `fish_batch`
  ADD PRIMARY KEY (`FBID`),
  ADD KEY `fishID` (`fishID`);

--
-- Indexes for table `fish_tank`
--
ALTER TABLE `fish_tank`
  ADD PRIMARY KEY (`tankID`),
  ADD KEY `FBID` (`FBID`),
  ADD KEY `plantID` (`plantID`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`notifID`);

--
-- Indexes for table `plant`
--
ALTER TABLE `plant`
  ADD PRIMARY KEY (`plantID`);

--
-- Indexes for table `record_archive`
--
ALTER TABLE `record_archive`
  ADD PRIMARY KEY (`RAID`);

--
-- Indexes for table `sensor`
--
ALTER TABLE `sensor`
  ADD PRIMARY KEY (`sensorID`);

--
-- Indexes for table `sensor_logs`
--
ALTER TABLE `sensor_logs`
  ADD PRIMARY KEY (`SensorLogID`),
  ADD KEY `sensorID` (`sensorID`),
  ADD KEY `tankID` (`tankID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userID`);

--
-- Indexes for table `user_tank`
--
ALTER TABLE `user_tank`
  ADD PRIMARY KEY (`UTID`),
  ADD KEY `userID` (`userID`),
  ADD KEY `tankID` (`tankID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_archive`
--
ALTER TABLE `activity_archive`
  MODIFY `AAID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `batch_bridge`
--
ALTER TABLE `batch_bridge`
  MODIFY `BBID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fish`
--
ALTER TABLE `fish`
  MODIFY `fishID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `fish_batch`
--
ALTER TABLE `fish_batch`
  MODIFY `FBID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `fish_tank`
--
ALTER TABLE `fish_tank`
  MODIFY `tankID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `notifID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sensor`
--
ALTER TABLE `sensor`
  MODIFY `sensorID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `sensor_logs`
--
ALTER TABLE `sensor_logs`
  MODIFY `SensorLogID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `userID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user_tank`
--
ALTER TABLE `user_tank`
  MODIFY `UTID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `batch_bridge`
--
ALTER TABLE `batch_bridge`
  ADD CONSTRAINT `batch_bridge_ibfk_1` FOREIGN KEY (`FBID`) REFERENCES `fish_batch` (`FBID`),
  ADD CONSTRAINT `batch_bridge_ibfk_2` FOREIGN KEY (`fishID`) REFERENCES `fish` (`fishID`);

--
-- Constraints for table `fish_tank`
--
ALTER TABLE `fish_tank`
  ADD CONSTRAINT `fish_tank_ibfk_1` FOREIGN KEY (`FBID`) REFERENCES `fish_batch` (`FBID`),
  ADD CONSTRAINT `fish_tank_ibfk_2` FOREIGN KEY (`plantID`) REFERENCES `plant` (`plantID`);

--
-- Constraints for table `sensor_logs`
--
ALTER TABLE `sensor_logs`
  ADD CONSTRAINT `sensor_logs_ibfk_1` FOREIGN KEY (`tankID`) REFERENCES `fish_tank` (`tankID`),
  ADD CONSTRAINT `sensor_logs_ibfk_2` FOREIGN KEY (`sensorID`) REFERENCES `sensor` (`sensorID`);

--
-- Constraints for table `user_tank`
--
ALTER TABLE `user_tank`
  ADD CONSTRAINT `user_tank_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `user` (`userID`),
  ADD CONSTRAINT `user_tank_ibfk_2` FOREIGN KEY (`tankID`) REFERENCES `fish_tank` (`tankID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
