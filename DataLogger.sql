--
-- Database: `DataLogger`
--
CREATE DATABASE IF NOT EXISTS `DataLogger` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `DataLogger`;

-- --------------------------------------------------------

--
-- Table structure for table `WeatherLink`
--


CREATE TABLE IF NOT EXISTS `WeatherLink` (
`id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deviceid` int(11) NOT NULL,
  `channel1_load_voltage` float NOT NULL,
  `channel1_current` float NOT NULL,
  `channel2_load_voltage` float NOT NULL,
  `channel2_current` float NOT NULL,
  `channel3_load_voltage` float NOT NULL,
  `channel3_current` float NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=96577 DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `WeatherLink`
--
ALTER TABLE `WeatherLink`
 ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `WeatherLink`
--
ALTER TABLE `WeatherLink`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=96577;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
