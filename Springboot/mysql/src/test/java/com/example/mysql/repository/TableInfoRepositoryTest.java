package com.example.mysql.repository;

import com.example.mysql.dto.TableInfoDto;
import com.example.mysql.model.TableInfo;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.annotation.Rollback;

import java.util.List;

@SpringBootTest
class TableInfoRepositoryTest {

    @Autowired
    TableInfoRepository testRepository;

    @Autowired
    JdbcTemplate jdbcTemplate;

    @Test
    @Rollback
    public void testSample() {

        // 动态检索
        TableInfoDto condition = new TableInfoDto();
        condition.setTableName("FIREEMBLEM_HERO");
        condition.setColFifterable("1");

        int searchCount = testRepository.getCountByDto(condition);
        List<TableInfo> resultList = testRepository.selectByDto(condition);
        Assert.assertEquals(resultList.size(), searchCount);

    }

    @Test
    public void testJdbcTemplate(){
        String query = "SELECT DISTINCT NAME_CN,NAME,NAME_JP FROM FIREEMBLEM_HERO WHERE NAME = ?";
        List<Object[]> queryResult = jdbcTemplate.query(query, (rs, rowNum) -> new Object[]{
                rs.getString("NAME_CN"),
                rs.getString("NAME"),
                rs.getString("NAME_JP")
        });
        for(Object[] row: queryResult) {
            //String[] columns = (String[]) row;
            System.out.println(row[0] + ";" + row[1] + ";" + row[2]);
        }
    }
}
