/*
 Navicat Premium Data Transfer

 Source Server         : 本地postgre
 Source Server Type    : PostgreSQL
 Source Server Version : 140013
 Source Host           : 127.0.0.1:5432
 Source Catalog        : postgres
 Source Schema         : paqu

 Target Server Type    : PostgreSQL
 Target Server Version : 140013
 File Encoding         : 65001

 Date: 16/03/2025 21:07:45
*/


-- ----------------------------
-- Table structure for conf
-- ----------------------------
DROP TABLE IF EXISTS "paqu"."conf";
CREATE TABLE "paqu"."conf" (
  "program" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "program_comment" varchar COLLATE "pg_catalog"."default",
  "key" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "key_comment" varchar COLLATE "pg_catalog"."default",
  "value" varchar COLLATE "pg_catalog"."default",
  "value_comment" varchar COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "paqu"."conf"."program" IS '程序名称';
COMMENT ON COLUMN "paqu"."conf"."program_comment" IS '程序名称注释';
COMMENT ON COLUMN "paqu"."conf"."key" IS '配置key';
COMMENT ON COLUMN "paqu"."conf"."key_comment" IS '配置key说明';
COMMENT ON COLUMN "paqu"."conf"."value" IS '配置value';
COMMENT ON COLUMN "paqu"."conf"."value_comment" IS '配置value说明';
COMMENT ON TABLE "paqu"."conf" IS '配置文件表';

-- ----------------------------
-- Records of conf
-- ----------------------------
INSERT INTO "paqu"."conf" VALUES ('yasuo', NULL, 'limit', NULL, '100', NULL);
INSERT INTO "paqu"."conf" VALUES ('douyin_paqu', '抖音爬取', 'is_headless', '', '0', NULL);
INSERT INTO "paqu"."conf" VALUES ('douyin_paqu', '抖音爬取', 'download_path', NULL, 'F:\douyin', NULL);
INSERT INTO "paqu"."conf" VALUES ('yasuo', NULL, 'source', '', 'F:\douyin', NULL);
INSERT INTO "paqu"."conf" VALUES ('yasuo', NULL, 'dest', '', 'F:\douyin_7z', NULL);
INSERT INTO "paqu"."conf" VALUES ('bilibili_paqu', 'b站爬取', 'cookie', NULL, '', 'b站爬取cookie');
INSERT INTO "paqu"."conf" VALUES ('bilibili_paqu', 'b站爬取', 'download_path', NULL, 'F:\bilibili', 'p站视频下载路径');

-- ----------------------------
-- Primary Key structure for table conf
-- ----------------------------
ALTER TABLE "paqu"."conf" ADD CONSTRAINT "conf_pkey" PRIMARY KEY ("program", "key");
