CREATE DATABASE  IF NOT EXISTS `bhkk4fwzoez0vzabscff` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bhkk4fwzoez0vzabscff`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: bhkk4fwzoez0vzabscff-mysql.services.clever-cloud.com    Database: bhkk4fwzoez0vzabscff
-- ------------------------------------------------------
-- Server version	8.0.22-13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'a05a675a-1414-11e9-9c82-cecd01b08c7e:1-491550428,
a38a16d0-767a-11eb-abe2-cecd029e558e:1-552668584';

--
-- Table structure for table `administradores`
--

DROP TABLE IF EXISTS `administradores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administradores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administradores`
--

LOCK TABLES `administradores` WRITE;
/*!40000 ALTER TABLE `administradores` DISABLE KEYS */;
INSERT INTO `administradores` VALUES (4,'admin_prueba@example.com','scrypt:32768:8:1$ODGpQStNphgxOrW5$8f729bdfd8175a7866f5280fad50476c4750a9df9f623306525b5a8b10e9fb66ae049be7e529f49279fc80a41903d58ad8210b4e2ca38f5d10c70aa8bf4f63f7'),(5,'bernacohd@gmail.com','scrypt:32768:8:1$CSF97x9lWeV19Ini$f689ec10ea2e3cb40538b7b9c7df7f15414d962ec5e31ef745cc22ed426cb2dea5b96d6043687486f31c53c1b483a4b96ac28c518aa775fa4ee23c9162de92d5');
/*!40000 ALTER TABLE `administradores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carrito`
--

DROP TABLE IF EXISTS `carrito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carrito` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL DEFAULT '1',
  `fecha_agregado` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrito`
--

LOCK TABLES `carrito` WRITE;
/*!40000 ALTER TABLE `carrito` DISABLE KEYS */;
INSERT INTO `carrito` VALUES (88,11,26,1,'2025-05-26 08:36:45'),(96,12,39,1,'2025-05-28 13:31:30');
/*!40000 ALTER TABLE `carrito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (1,'Escayolas3D'),(2,'Almacenaje'),(3,'Herramientas'),(4,'Gadgets'),(5,'Juguetes'),(6,'Decoracion');
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido_detalles`
--

DROP TABLE IF EXISTS `pedido_detalles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido_detalles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `pedido_detalles_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedido_detalles_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_detalles`
--

LOCK TABLES `pedido_detalles` WRITE;
/*!40000 ALTER TABLE `pedido_detalles` DISABLE KEYS */;
INSERT INTO `pedido_detalles` VALUES (28,16,26,2,39.98),(32,17,26,1,19.99),(37,18,26,8,39.92),(38,19,59,3,359.97),(39,19,40,3,59.97),(40,19,41,1,24.99),(41,19,47,1,12.99),(42,19,57,1,75.99),(43,20,47,3,38.97),(44,20,53,2,199.98),(45,20,54,1,33.99),(46,21,57,1,75.99),(47,22,58,1,99.99),(48,22,39,2,13.98),(49,22,55,1,21.99),(50,23,57,1,75.99),(51,23,26,1,4.99),(52,23,58,1,99.99),(53,24,43,2,3.98),(54,25,43,50,99.50),(55,26,58,1,99.99),(56,27,56,15,554.85),(57,28,54,17,577.83),(58,28,58,69,6899.31),(59,29,39,2,13.98),(60,30,50,2,53.98),(61,31,51,40,119.60),(62,32,43,1,1.99),(63,33,51,2,5.98),(64,33,57,1,75.99),(65,33,59,1,119.99),(66,33,41,3,74.97),(67,34,26,1,4.99),(68,35,39,1,6.99),(69,36,59,4,479.96),(70,36,39,6,41.94),(71,36,50,2,53.98),(72,37,58,7,699.93),(73,38,59,1,119.99);
/*!40000 ALTER TABLE `pedido_detalles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `fecha_pedido` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `estado_pago` enum('Pendiente','Procesando','Pagado') DEFAULT 'Pendiente',
  `estado` enum('Procesando','Enviado','Completado','Cancelado') DEFAULT 'Procesando',
  `total` decimal(10,2) NOT NULL,
  `numero_pedido` varchar(10) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `ciudad` varchar(100) NOT NULL,
  `codigo_postal` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_pedido` (`numero_pedido`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (15,7,'2025-05-16 10:42:18','Pendiente','Procesando',123.22,'ES000001','Calixto III','Valencia','46008'),(16,8,'2025-05-16 10:53:25','Pendiente','Procesando',644.86,'ES000002','Calixto III','Valencia','0001'),(17,10,'2025-05-16 11:17:44','Pendiente','Procesando',50124.96,'ES000003','Calle 303 num 19','Valencia','46182'),(18,7,'2025-05-19 13:05:14','Pendiente','Procesando',39.92,'ES000004','Calixto III','Valencia','46008'),(19,8,'2025-05-19 14:28:38','Pendiente','Procesando',533.91,'ES000005','Calixto III','Valencia','0001'),(20,7,'2025-05-19 14:39:15','Pendiente','Procesando',272.94,'ES000006','Calixto III','Valencia','46008'),(21,7,'2025-05-19 15:52:49','Pendiente','Procesando',75.99,'ES000007','Calixto III','Valencia','46008'),(22,7,'2025-05-20 12:06:40','Pendiente','Procesando',135.96,'ES000008','Calixto III','Valencia','46008'),(23,11,'2025-05-22 15:02:25','Pendiente','Procesando',180.97,'ES000009','Calixto III 34/26','Valencia','46008'),(24,11,'2025-05-22 15:23:59','Pendiente','Procesando',3.98,'ES000010','Calixto III 34/26','Valencia','46008'),(25,7,'2025-05-23 11:19:58','Pendiente','Procesando',99.50,'ES000011','Calixto III','Valencia','46008'),(26,7,'2025-05-23 14:06:45','Pendiente','Procesando',99.99,'ES000012','Calixto III','Valencia','46008'),(27,12,'2025-05-23 14:07:46','Pendiente','Procesando',554.85,'ES000013','Calle Mislata 56','Xirivella','45980'),(28,12,'2025-05-23 14:17:00','Pendiente','Procesando',7477.14,'ES000014','Calle Mislata 56','Xirivella','45980'),(29,7,'2025-05-23 20:22:09','Pendiente','Procesando',13.98,'ES000015','Calixto III','Valencia','46008'),(30,7,'2025-05-24 18:50:34','Pendiente','Procesando',53.98,'ES000016','Calixto III','Valencia','46008'),(31,7,'2025-05-26 14:08:38','Pendiente','Procesando',119.60,'ES000017','Calixto III','Valencia','46008'),(32,7,'2025-05-26 14:22:13','Pendiente','Procesando',1.99,'ES000018','Calixto III','Valencia','46008'),(33,14,'2025-05-28 13:32:40','Pendiente','Procesando',276.93,'ES000019','Avda Pérez Galdós 77-20','Valencia','46018'),(34,14,'2025-05-28 13:34:10','Pendiente','Procesando',4.99,'ES000020','Avda Pérez Galdós 77-20','Valencia','46018'),(35,7,'2025-05-28 14:25:27','Pendiente','Procesando',6.99,'ES000021','Calixto III','Valencia','46008'),(36,7,'2025-05-28 15:10:35','Pendiente','Procesando',575.88,'ES000022','Calixto III','Valencia','46008'),(37,7,'2025-05-28 15:12:02','Pendiente','Procesando',699.93,'ES000023','Calixto III','Valencia','46008'),(38,7,'2025-05-28 15:30:45','Pendiente','Procesando',119.99,'ES000024','Calixto III','Valencia','46008');
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(255) NOT NULL,
  `descripcion` text NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `imagenes` text NOT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `categoria_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (26,'Portapilas AA','Seguridad y Rendimiento para tus Dispositivos Optimiza el funcionamiento de tus aparatos electrónicos con nuestro portapilas de alta calidad. Diseñado en plástico resistente con contactos metálicos eficientes, garantiza una conexión segura y estable. Compatible con una amplia gama de dispositivos, desde juguetes hasta equipos electrónicos.',6.99,'https://i.postimg.cc/mrMyfMK7/imagen-2025-05-19-141142256.png','2025-05-09 13:36:56',2),(37,'USB SD and MicroSD holder for wide USB sticks','Este soporte admite 8 memorias USB anchas, 8 tarjetas SD y hasta 15 tarjetas MicroSD.\r\n\r\nIdeal para tu escritorio, para mantener tu almacenamiento portátil en un solo lugar cuando lo necesites.\r\n\r\nTiene orificios para evitar la acumulación de polvo y reducir ligeramente el material de impresión.',9.99,'https://i.postimg.cc/G2vz8rNs/imagen-2025-05-22-122436573.png','2025-05-19 12:07:21',2),(38,'Caja apilable V4','Este es un remix del modelo de Gushie (http://www.thingiverse.com/thing:447213), que a su vez es un remix del modelo de 1986breeze (http://www.thingiverse.com/thing:234669), que a su vez es un remix del modelo de martinhering (http://www.thingiverse.com/thing:177814).\r\n\r\nReforcé el borde frontal y ajusté el diseño para aumentar la estabilidad al apilar. El resultado debería ser una mejora drástica en la apilabilidad, sin un aumento significativo en el uso de material ni en el tiempo de impresión. El diseño es totalmente compatible con las versiones de Gushie y 1986breeze (ya que se apilan).\r\n\r\nTambién añadí una versión con una partición central y bandejas extraíbles para objetos pequeños y puntas de destornillador.',13.99,'https://i.postimg.cc/P5FKWdnF/imagen-2025-05-19-142446358.png','2025-05-19 12:24:54',2),(39,'Caja UNO','Mantén tus objetos protegidos y bien organizados con nuestra caja pequeña de alta calidad. Fabricada con materiales resistentes, ideal para almacenar joyas, accesorios, herramientas o cualquier pequeño tesoro. Su diseño compacto permite llevarla fácilmente en bolsos, mochilas o mantenerla en el escritorio.',6.99,'https://i.postimg.cc/zGpsvwW1/imagen-2025-05-22-122311278.png','2025-05-19 12:27:04',2),(40,'Set de Contenedores en Forma de Hongo','Diseño Divertido y Funcional Guarda tus objetos con estilo y nostalgia con estos contenedores inspirados en los famosos hongos de los videojuegos. Fabricados en impresión 3D con materiales resistentes, son ideales para almacenar pequeños tesoros como monedas, accesorios o piezas electrónicas.\r\nPerfectos para regalar... hasta que algún fontanero famoso llame a su abogado. ¡Consíguelos antes de que desaparezcan misteriosamente!',19.99,'https://i.postimg.cc/pLrVcMpF/imagen-2025-05-19-150642634.png','2025-05-19 12:30:23',2),(41,'Dispensador de té ','Dispensador de Té – Sabor y Comodidad en Cada Taza Disfruta de la perfección en cada infusión con nuestro dispensador de té práctico y elegante. Diseñado para facilitar la preparación de tu bebida favorita, permite un vertido preciso y sin desperdicios. Ideal para hogares, oficinas o cualquier rincón dedicado al bienestar y la relajación.',24.99,'https://i.postimg.cc/zfwQnV8S/imagen-2025-05-19-150840412.png','2025-05-19 12:32:29',2),(42,'Abrazaderas de Alta Resistencia','Seguridad y Fijación en Cada Uso Maximiza la estabilidad y durabilidad de tus instalaciones con nuestras abrazaderas de alta calidad. Diseñadas para ofrecer un ajuste firme y seguro, son perfectas para organizar cables, sujetar tuberías o reforzar estructuras.',18.99,'https://i.postimg.cc/63B0wqrq/imagen-2025-05-19-143438634.png','2025-05-19 12:34:45',3),(43,'Plantilla de Marcado para Carpintería','Precisión en Cada Corte Haz que tus proyectos de carpintería sean más precisos con nuestra plantilla de marcado profesional. Diseñada para facilitar la trazabilidad de líneas exactas en madera, esta herramienta es indispensable para quienes buscan cortes y ensamblajes impecables.',1.99,'https://i.postimg.cc/1zSC5swg/imagen-2025-05-19-150944100.png','2025-05-19 12:36:47',3),(44,'CNC \"MPCNC\" Burly F-25 mm OD','Precisión y Versatilidad en Fabricación Domina el arte del corte y grabado con la CNC \"MPCNC\" Burly, un diseño modular y eficiente con piezas impresas en 3D para una estructura adaptable y personalizable. Perfecta para trabajos en madera, plásticos y metales suaves, su construcción optimizada permite un rendimiento excepcional sin comprometer la accesibilidad.',249.99,'https://i.postimg.cc/bwbHtkLd/imagen-2025-05-19-143735399.png','2025-05-19 12:38:31',3),(45,' Raptor recargado por e-NABLE','Si bien el Raptor Reloaded ha sido un diseño muy popular en la comunidad e-NABLE, ya no se recomienda su uso, salvo para fines de prueba e investigación. Las pruebas han demostrado que su capacidad de agarre no es tan buena como la de los diseños e-NABLE más recientes.\r\n',54.99,'https://i.postimg.cc/pT6J8HhJ/imagen-2025-05-19-151020269.png','2025-05-19 12:39:36',3),(46,'Cargador de teléfono Tesla SuperCharger','Energía Rápida, Estilo Futurista Lleva la velocidad de carga a otro nivel con el Tesla SuperCharger para teléfonos. Inspirado en la icónica tecnología de carga ultrarrápida de Tesla, este cargador combina diseño moderno y rendimiento eficiente, ideal para mantener tu dispositivo con energía en cualquier momento.',17.99,'https://i.postimg.cc/2SFLYw2d/imagen-2025-05-19-144027236.png','2025-05-19 12:41:01',4),(47,'¡Abridor de botellas y pistola de tapones!','Diversión y Funcionalidad en un Solo Dispositivo Convierte cada descorche en una experiencia inolvidable con este abridor de botellas con función de pistola de tapones. No solo destapas tu bebida con facilidad, sino que además puedes lanzar el corcho o la chapa con precisión y estilo. Perfecto para reuniones, fiestas o simplemente para darle un toque divertido a cada brindis.',12.99,'https://i.postimg.cc/0NVnCmKv/imagen-2025-05-19-144137442.png','2025-05-19 12:42:04',4),(48,'Estuche BabyNES para Raspberry Pi B+','Retro y Funcionalidad en un Solo Diseño Revive la nostalgia de los videojuegos clásicos mientras proteges tu Raspberry Pi B+ con este estuche BabyNES. Inspirado en la icónica consola de Nintendo, su diseño compacto y detallado le da un toque vintage a tu mini PC sin comprometer la accesibilidad a los puertos y la ventilación.',34.99,'https://i.postimg.cc/MH7j923B/imagen-2025-05-19-144239259.png','2025-05-19 12:43:12',4),(49,'R2D2 Google Home Mini','La Fuerza de la Tecnología en Tu Hogar Convierte tu asistente virtual en el droide más fiel de la galaxia con este estuche R2D2 para Google Home Mini. Con un diseño inspirado en el icónico droide de Star Wars, este accesorio no solo protege tu dispositivo, sino que le da un toque intergaláctico a cualquier espacio.',39.99,'https://i.postimg.cc/XNfGSWxG/imagen-2025-05-19-144410802.png','2025-05-19 12:44:54',4),(50,'Soporte para portátil reposicionable','Ligero, Potente y Totalmente Ajustable Optimiza tu espacio de trabajo con este soporte para portátil versátil, diseñado para ofrecer estabilidad, comodidad y máxima movilidad. Su estructura ligera pero resistente permite reposicionarlo fácilmente sin perder firmeza, ideal para adaptarse a distintas alturas y ángulos.',26.99,'https://i.postimg.cc/1txt27qr/imagen-2025-05-19-144533765.png','2025-05-19 12:45:59',4),(51,' ¡Chicos con auriculares!','Los soportes para auriculares son una forma práctica, divertida y genial de organizar tus auriculares. Olvídate de los cables desordenados, con estos pequeños accesorios para cuidarlos. Ideales como regalo o para usar en casa o de viaje. Hay dos versiones: una es un hombre con gafas de sol y la otra un extraterrestre... ¡solo por diversión!\r\n',2.99,'https://i.postimg.cc/sgvgXCPJ/imagen-2025-05-19-144657915.png','2025-05-19 12:47:12',4),(52,'Pokéball con Tapa de Liberación por Botón','Atrapa y Guarda con Estilo Guarda tus pequeños objetos con el toque mágico de un verdadero entrenador. Esta Pokéball con mecanismo de apertura por botón combina diseño nostálgico con funcionalidad moderna. Perfecta para almacenar monedas, accesorios o cualquier pequeño tesoro, su estructura resistente y su sistema de apertura suave garantizan comodidad y seguridad.\r\nPD: No garantizamos que esta Pokéball realmente atrape Pokémon, pero al menos guardarás cosas con estilo.',39.99,'https://i.postimg.cc/NGDskjp4/imagen-2025-05-19-144814607.png','2025-05-19 12:49:23',5),(53,'Miniatura Banana Knight','¡Dale un toque épico y divertido a tu colección con esta miniatura Banana Knight! Con una armadura medieval impecable y un escudo vibrante, este guerrero con cuerpo de banana es la combinación perfecta entre lo absurdo y lo legendario. Fabricado con gran atención al detalle, su base texturizada con musgo le da un aire de batalla fantástica.',99.99,'https://i.postimg.cc/3rfMw4tP/imagen-2025-05-19-145022656.png','2025-05-19 12:51:45',5),(54,'Pikachu Musculoso','¡El Pokémon más icónico ha pasado por el gimnasio y está listo para impresionar! Este Pikachu musculoso redefine la ternura con un físico de campeonato, luciendo una pose de culturismo que electrificará cualquier colección. Con detalles cuidadosamente esculpidos y un acabado vibrante, esta figura es perfecta para los fans que buscan algo único y divertido.',33.99,'https://i.postimg.cc/G29WPb2M/imagen-2025-05-19-145219353.png','2025-05-19 12:52:56',5),(55,'Preciosa decoración de pared de gato.','Añade un toque de sofisticación y ternura a tu hogar con esta preciosa decoración de pared de gato. Con un diseño artístico y detallado, esta pieza captura la belleza y el misterio de los felinos, convirtiéndola en un elemento perfecto para cualquier espacio.',21.99,'https://i.postimg.cc/9f08KJh0/imagen-2025-05-19-145421544.png','2025-05-19 12:54:32',6),(56,'Jarrón de flores Trivo de MODERN MACHINE','Dale un toque sofisticado a tu espacio con el Jarrón de Flores Trivo, una pieza única diseñada por MODERN MACHINE',36.99,'https://i.postimg.cc/rp9VZyqM/imagen-2025-05-19-145829758.png','2025-05-19 12:59:09',6),(57,'El rincón del dragón emergente – Edición Cabeza y Cola','Transforma tu estantería en un escenario épico con El Rincón del Dragón Emergente. Esta impresionante pieza de decoración captura la esencia de la fantasía con una cabeza y cola de dragón que parecen salir de entre los libros. Perfecto para los amantes de la literatura fantástica y la impresión 3D, este diseño añade un toque mágico a cualquier espacio.',75.99,'https://i.postimg.cc/cJ7RD3KC/imagen-2025-05-19-150136447.png','2025-05-19 13:02:36',6),(58,'Escayola 3D para Niños','La recuperación de los pequeños ahora es más cómoda y divertida con nuestra escayola impresa en 3D. Diseñada para ofrecer soporte, protección y libertad, su estructura ventilada y resistente al agua permite que los niños disfruten de actividades diarias sin restricciones.',99.99,'https://i.postimg.cc/nLKf2nvZ/imagen-2025-05-19-161424345.png','2025-05-19 14:15:30',1),(59,'Escayolas modulares','Diseñadas para ajustarse a distintas formas y tamaños, ideales para varios usos y comoda',119.99,'https://i.postimg.cc/Bv4VqHK9/imagen-2025-05-19-161601336.png','2025-05-19 14:17:13',1),(60,'Escayolas flexibles','Fabricadas con materiales que permiten cierta movilidad sin perder resistencia.',149.99,'https://i.postimg.cc/CKMpcWJq/imagen-2025-05-19-161729363.png','2025-05-19 14:17:54',1);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_completo` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contraseña` text NOT NULL,
  `direccion_completa` varchar(255) NOT NULL,
  `ciudad` varchar(100) NOT NULL,
  `codigo_postal` varchar(10) NOT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `reset_token` varchar(255) DEFAULT NULL,
  `reset_token_expiration` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (7,'Arturo Orient Romero','arturorient1305@gmail.com','scrypt:32768:8:1$63vXMxfnwlNz3bP4$3a6d550a4820477e03f8298194461ea3a817827b310790f72b4dedc53c38da95006a12bb3414a13aaacaac47f7a71310df9360f6bf5f3e2a91da9d3d76ff78dd','Calixto III','Valencia','46008','2025-05-13 15:12:07',NULL,'2025-05-23 11:50:18'),(8,'Josefa Romero Rivas','bernacoxd@gmail.com','scrypt:32768:8:1$Q3RendOiNuCM5S4O$ea4215df62118bfda3db8c7a3f2e0fb97821467ede238f028153633355d60dd46b846f83127e29b3e3b2a7917680c8dd80e63643659edbccc964d51009665788','Calixto III','Valencia','0001','2025-05-13 15:50:28',NULL,'2025-05-14 12:37:17'),(10,'Adrián Zarco Martínez','zarcoadrian59@gmail.com','scrypt:32768:8:1$7ky7TlYFbkQkxiVD$bfe8a5dd8c12a8c431ac23a6c2978addb3bd1677e3274e02e0bd95ad4b56468b5694ece381fbbd9d78c58348261052795da93a39cfd696b053e527d452d9c902','Calle 303 num 19','Valencia','46182','2025-05-16 11:07:46',NULL,NULL),(11,'Hela','bernacohd@gmail.com','scrypt:32768:8:1$rTZcXkQH4vPedFjr$e96921cb42fb6c78ff35e37764de59a56f188555dbec352938728089bc4d888e6d672cb5f6e0823127a538b73203a5846df085a75a948f6da4212686b9d9b1fa','Calixto III 34/26','Valencia','46008','2025-05-22 14:17:05',NULL,'2025-05-22 16:48:13'),(12,'David Kalmuk','davidkalmuk65@gmail.com','scrypt:32768:8:1$bzKgMWUhah7i7W7g$1bfe8306fd1bd41a4bd45fad89fcf22980fb124e70e083c9641e89f593e0f19ddc408ca0405706a689d23418251e57721e0d136212a267d0731ac7caf7fde10f','Calle Mislata 56','Xirivella','45980','2025-05-23 11:19:27',NULL,'2025-05-28 14:00:28'),(13,'Adolfo Mr.Potato','patata2991@gmail.com','scrypt:32768:8:1$0WVmFNEtLHSh3YjG$a851a93739e7ddde53e0cc8508fbd1cf66a488221289ddd0a74e5fb18918f3eb61e09965548c2ef820ce6c4e7bf9afeea40cb623050325d8748b330631dc0442','Calle Real de la Alberga,Alcorcon','Alcorcon','28921','2025-05-23 11:56:34',NULL,NULL),(14,'Diana Pérez Gimeno','nuchi192@hotmail.com','scrypt:32768:8:1$jGQ3pXwVsNm5BEkm$96f207d07dcfd28e4250a63e7129cd73c647b73c1ea6ecaa91c7d7acf758ea0355d9ec39750493d9f392c14c7ca7f9e1ab3e8903a3f5f05c6654e161bfb04ccd','Avda Pérez Galdós 77-20','Valencia','46018','2025-05-28 13:19:33',NULL,NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valoraciones`
--

DROP TABLE IF EXISTS `valoraciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valoraciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `valor` float NOT NULL,
  `comentario` text,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `valoraciones_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `valoraciones_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `valoraciones_chk_1` CHECK ((`valor` between 1 and 5))
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valoraciones`
--

LOCK TABLES `valoraciones` WRITE;
/*!40000 ALTER TABLE `valoraciones` DISABLE KEYS */;
INSERT INTO `valoraciones` VALUES (1,26,7,3,'A','2025-05-14 14:06:43'),(2,26,7,5,'Prueba NºPerdi la cuenta','2025-05-14 14:15:11'),(3,26,8,1,'Prueba con  otra cuenta','2025-05-14 14:20:18'),(5,26,8,1,'p','2025-05-14 14:30:51'),(6,26,8,1,'p','2025-05-14 14:30:58'),(11,26,7,5,'Buen producto','2025-05-15 10:58:36'),(12,26,7,5,'Buen producto','2025-05-15 10:58:38'),(13,26,10,1,'El producto esta muy bien se nota que es de calidad pero el problema fue que mi hermano se tiro por la ventana y se dejo los dientes.\r\nPostdata:\r\nLo recomiendo es muy bueno pero aten a sus hermanos a una silla.','2025-05-16 11:12:08'),(18,47,7,3,'!','2025-05-19 13:44:56'),(19,47,7,5,'Gran Producto','2025-05-19 13:45:07'),(20,40,8,4,'El Producto Mola','2025-05-19 13:46:03'),(21,54,8,5,'Nop hay Nada malo que comentar de este producto :)','2025-05-19 13:46:49'),(22,57,8,4,'Me parece un fantastico producto','2025-05-19 14:27:03'),(23,57,11,5,'Me encanta','2025-05-22 14:26:52'),(24,58,11,5,'Gran producto a mi hijo le encanta','2025-05-22 15:02:02'),(25,50,13,5,'Fantástico,desde que lo tengo mi portatil ya no me produce quemaduras en la mano por el uso, muy recomendable.','2025-05-23 11:57:36'),(26,39,7,5,'Me encanta es ideal. Bonito por fuera y muy práctico por dentro. Cari es lo masss','2025-05-23 20:19:54'),(27,57,7,5,'Gran Producto!!!','2025-05-26 14:09:15'),(28,57,14,5,'Me parece un producto super original, tanto por la decoración, como por lo práctico que es','2025-05-28 13:26:25'),(29,59,14,5,'Me parece una idea estupenda ya que se puede ir aumentando o disminuyendo la escayola según la necesidad','2025-05-28 13:28:11'),(30,41,14,5,'Super práctico para tener todas las infusiones a la vista y a mano. El único pero que pondría es que si está incompleta de cajas, se caen','2025-05-28 13:31:29');
/*!40000 ALTER TABLE `valoraciones` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-30 11:29:57
