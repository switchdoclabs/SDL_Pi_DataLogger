
-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 19, 2016 at 01:30 AM
-- Server version: 5.5.44-0+deb8u1
-- PHP Version: 5.6.22-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `DataLogger`
--
CREATE DATABASE IF NOT EXISTS `DataLogger` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `DataLogger`;

-- --------------------------------------------------------

--
-- Table structure for table `ADS1115Table`
--

DROP TABLE IF EXISTS `ADS1115Table`;
CREATE TABLE IF NOT EXISTS `ADS1115Table` (
`id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deviceid` int(11) NOT NULL,
  `channel0_voltage` float NOT NULL,
  `channel0_raw` int(11) NOT NULL,
  `channel1_voltage` float NOT NULL,
  `channel1_raw` int(11) NOT NULL,
  `channel2_voltage` float NOT NULL,
  `channel2_raw` int(11) NOT NULL,
  `channel3_voltage` float NOT NULL,
  `channel3_raw` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `INA3221Table`
--

DROP TABLE IF EXISTS `INA3221Table`;
CREATE TABLE IF NOT EXISTS `INA3221Table` (
`id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deviceid` int(11) NOT NULL,
  `channel1_load_voltage` float NOT NULL,
  `channel1_current` float NOT NULL,
  `channel2_load_voltage` float NOT NULL,
  `channel2_current` float NOT NULL,
  `channel3_load_voltage` float NOT NULL,
  `channel3_current` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `OURWEATHERTable`
--

DROP TABLE IF EXISTS `OURWEATHERTable`;
CREATE TABLE IF NOT EXISTS `OURWEATHERTable` (
`ID` int(20) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deviceid` int(11) NOT NULL,
  `Outdoor_Temperature` float NOT NULL,
  `Outdoor_Humidity` float NOT NULL,
  `Indoor_Temperature` float NOT NULL,
  `Barometric_Pressure` float NOT NULL,
  `Altitude` float NOT NULL,
  `Current_Wind_Speed` float NOT NULL,
  `Current_Wind_Gust` float NOT NULL,
  `Current_Wind_Direction` float NOT NULL,
  `Rain_Total` float NOT NULL,
  `Wind_Speed_Minimum` float NOT NULL,
  `Wind_Speed_Maximum` float NOT NULL,
  `Wind_Gust_Minimum` float NOT NULL,
  `Wind_Gust_Maximum` float NOT NULL,
  `Wind_Direction_Minimum` float NOT NULL,
  `Wind_Direction_Maximum` float NOT NULL,
  `Display_English_Metrice` int(11) NOT NULL,
  `OurWeather_DateTime` varchar(30) NOT NULL,
  `OurWeather_Station_Name` varchar(30) NOT NULL,
  `Current_Air_Quality_Sensor` int(11) NOT NULL,
  `Current_Air_Quality_Qualitative` int(11) NOT NULL,
  `Battery_Voltage` float NOT NULL,
  `Battery_Current` float NOT NULL,
  `Solar_Voltage` float NOT NULL,
  `Solar_Current` float NOT NULL,
  `Load_Voltage` float NOT NULL,
  `Load_Current` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='OurWeather FullDataString';

-- --------------------------------------------------------

--
-- Table structure for table `ThreePanelTestTable`
--

DROP TABLE IF EXISTS `ThreePanelTestTable`;
CREATE TABLE IF NOT EXISTS `ThreePanelTestTable` (
`id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deviceid` int(11) NOT NULL,
  `channel1_load_voltage` float NOT NULL,
  `channel1_current` float NOT NULL,
  `channel2_load_voltage` float NOT NULL,
  `channel2_current` float NOT NULL,
  `channel3_load_voltage` float NOT NULL,
  `channel3_current` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `WXLINKTable`
--

DROP TABLE IF EXISTS `WXLINKTable`;
CREATE TABLE IF NOT EXISTS `WXLINKTable` (
`ID` int(20) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deviceid` int(11) NOT NULL,
  `Protocol` int(11) NOT NULL,
  `Outdoor_Temperature` float NOT NULL,
  `Outdoor_Humidity` float NOT NULL,
  `Indoor_Temperature` float NOT NULL,
  `Barometric_Pressure` float NOT NULL,
  `Current_Wind_Speed` float NOT NULL,
  `Current_Wind_Clicks` int(11) NOT NULL,
  `Current_Wind_Direction` float NOT NULL,
  `Rain_Total_Clicks` int(11) NOT NULL,
  `Battery_Voltage` float NOT NULL,
  `Battery_Current` float NOT NULL,
  `Load_Current` float NOT NULL,
  `Solar_Panel_Voltage` float NOT NULL,
  `Solar_Panel_Current` float NOT NULL,
  `MessageID` int(11) NOT NULL,
  `Time_Since_Reboot` int(11) NOT NULL,
  `AuxA` float NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=11890 DEFAULT CHARSET=latin1 COMMENT='WXLIINK Dump data';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ADS1115Table`
--
ALTER TABLE `ADS1115Table`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `INA3221Table`
--
ALTER TABLE `INA3221Table`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `OURWEATHERTable`
--
ALTER TABLE `OURWEATHERTable`
 ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `ThreePanelTestTable`
--
ALTER TABLE `ThreePanelTestTable`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `WXLINKTable`
--
ALTER TABLE `WXLINKTable`
 ADD PRIMARY KEY (`ID`), ADD KEY `ID` (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ADS1115Table`
--
ALTER TABLE `ADS1115Table`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `INA3221Table`
--
ALTER TABLE `INA3221Table`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `OURWEATHERTable`
--
ALTER TABLE `OURWEATHERTable`
MODIFY `ID` int(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `ThreePanelTestTable`
--
ALTER TABLE `ThreePanelTestTable`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `WXLINKTable`
--
ALTER TABLE `WXLINKTable`
MODIFY `ID` int(20) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=11890;
