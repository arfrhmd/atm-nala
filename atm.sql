-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for atm
CREATE DATABASE IF NOT EXISTS `atm` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `atm`;

-- Dumping structure for table atm.rekening
CREATE TABLE IF NOT EXISTS `rekening` (
  `no_rekening` varchar(6) NOT NULL,
  `user_id` varchar(4) NOT NULL,
  `pin` char(6) NOT NULL,
  `tipe` enum('Giro','Tabungan') DEFAULT NULL,
  `saldo` decimal(11,2) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`no_rekening`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table atm.rekening: ~4 rows (approximately)
INSERT INTO `rekening` (`no_rekening`, `user_id`, `pin`, `tipe`, `saldo`, `updated_at`) VALUES
	('090602', '0906', '223344', 'Tabungan', 505000.00, '2023-07-02 04:43:23'),
	('180700', '1807', '555666', 'Tabungan', 1740000.00, '2023-07-02 04:46:53'),
	('210799', '2107', '998877', 'Tabungan', 1050000.00, '2023-07-02 04:43:23'),
	('300901', '3009', '111111', 'Tabungan', 2500000.00, '2023-07-02 04:46:53');

-- Dumping structure for table atm.transaksi
CREATE TABLE IF NOT EXISTS `transaksi` (
  `no_transaksi` int NOT NULL AUTO_INCREMENT,
  `rek_pengirim` varchar(6) NOT NULL,
  `rek_penerima` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipe` enum('Tarik Tunai','Setor Tunai','Transfer') DEFAULT NULL,
  `saldo` decimal(11,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`no_transaksi`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table atm.transaksi: ~3 rows (approximately)
INSERT INTO `transaksi` (`no_transaksi`, `rek_pengirim`, `rek_penerima`, `tipe`, `saldo`, `created_at`) VALUES
	(1, '180700', NULL, 'Setor Tunai', 1000000.00, '2023-07-05 13:56:06'),
	(2, '180700', NULL, 'Tarik Tunai', 5000.00, '2023-07-05 13:56:22'),
	(3, '180700', '90602', 'Transfer', 5000.00, '2023-07-05 13:56:37');

-- Dumping structure for table atm.user
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` varchar(4) NOT NULL,
  `email` varchar(50) NOT NULL,
  `nm_lengkap` varchar(100) NOT NULL,
  `nm_ibu` varchar(100) NOT NULL,
  `is_block` int NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table atm.user: ~4 rows (approximately)
INSERT INTO `user` (`user_id`, `email`, `nm_lengkap`, `nm_ibu`, `is_block`) VALUES
	('0906', 'arif@gmail.com', 'ARIF RAHMADI', 'SHANI', 0),
	('1807', 'aldi@gmail.com', 'ALDI RIVALDI', 'JESSICA', 1),
	('2107', 'anissa@gmail.com', 'ANISSA', 'RACHEL', 1),
	('3009', 'bunga@gmail.com', 'LIDYA BUNGA', 'FREYA', 0);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
