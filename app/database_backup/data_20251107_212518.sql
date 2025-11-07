-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: ecomdb
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` (`categoryid`, `name`) VALUES (1,'ELECTRONICS'),(2,'Home Appliances');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `categorys`
--

LOCK TABLES `categorys` WRITE;
/*!40000 ALTER TABLE `categorys` DISABLE KEYS */;
/*!40000 ALTER TABLE `categorys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` (`customerid`, `fname`, `lname`, `phoneno`, `password_hash`, `address`, `pincode`, `district`, `state`, `housename`) VALUES (100000,'Leo','Messi','7777777777','scrypt:32768:8:1$1jDHZrsd3LJWZdwi$ec7aed3b4879525141c677a2134eca080d360e0266db2bd11b538692e696a51d53906e4438eecd0b755feffca9bddc907a0dc9e713e11856a9ae8f7c3991e1bf','FCB','555555','FCB','FCB','FCB'),(100001,'John','Wick','9999999999','scrypt:32768:8:1$S2qx7B6MkJ5gGoos$cf22d71be3eec6b70169b2f48cd69b81f6422721a1abcb3be4269a25a8f649c900d1b8b1addc83b8ed7c4f5f4ae41ddddb0bb127d5edc90c51fa6b41d88d9265','NYC','888888','NYC','NYC','NYC'),(100002,'admin','admin','9999999998','scrypt:32768:8:1$CWYYAy9FohmYd07J$4148ec1630bec8c184b4bb500117d745c0cd23912c5c8a55c377f8ab00c1b4429ed08d4ab89d2bbf003ea911e75ca8dc70eee6454e5beab4e59bd9b16eca1aba','admin','888888','admin','admin','admin');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` (`orderid`, `customerid`, `productid`, `sellerid`, `qty`, `status`) VALUES (1,100001,1,1,1,'Delivered');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` (`productid`, `product_name`, `description`, `sellerid`, `subcategoryid`, `rating`, `stock`, `price`, `images_url`) VALUES (1,'Lenovo Laptop','Powerful 14th Generation Intel i7-14700HX 24-Core (Base Clock 2.2GHz, Up to 5.5GHz with Intel Turbo Boost Technology, 33MB Intel Smart Cache, 20 cores, 8 Performance-Cores, 16 Efficient-Cores, 28 threads)',1,3,0,749,120000,'https://pyrimbctohsuqqxqtehq.supabase.co/storage/v1/object/public/product-images/1762452505553_ilfloy3wwcuwumbgnbaany1217gn2p769424.avif');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` (`reviewid`, `productid`, `customerid`, `rating`, `comment`, `created_at`) VALUES (1,1,100001,5,'phenomenal','2025-11-07 01:27:22');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `sellers`
--

LOCK TABLES `sellers` WRITE;
/*!40000 ALTER TABLE `sellers` DISABLE KEYS */;
INSERT INTO `sellers` (`sellerid`, `customerid`, `rating`) VALUES (1,100000,0);
/*!40000 ALTER TABLE `sellers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `subcategories`
--

LOCK TABLES `subcategories` WRITE;
/*!40000 ALTER TABLE `subcategories` DISABLE KEYS */;
INSERT INTO `subcategories` (`subcategoryid`, `name`, `categoryid`) VALUES (1,'Mobiles',1),(2,'TV',1),(3,'Laptops',1),(4,'Fridge',2);
/*!40000 ALTER TABLE `subcategories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `subcategorys`
--

LOCK TABLES `subcategorys` WRITE;
/*!40000 ALTER TABLE `subcategorys` DISABLE KEYS */;
/*!40000 ALTER TABLE `subcategorys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` (`transid`, `orderid`, `customerid`, `amount`, `status`, `transDate`) VALUES (1,1,100001,120000,'Completed','2025-11-06 18:09:14');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-07 21:25:20
