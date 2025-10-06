package com.example.sqlite;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.example.sqlite.repository")
public class SqliteApplication {

    public static void main(String[] args) {
        SpringApplication.run(SqliteApplication.class, args);
    }

}
