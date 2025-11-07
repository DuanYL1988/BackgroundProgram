package com.example.mysql.repository;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.test.annotation.Rollback;

import com.example.mysql.dto.TableInfoDto;
import com.example.mysql.model.TableInfo;

@SpringBootTest
class TableInfoRepositoryTest {

    @Autowired
    TableInfoRepository testRepository;

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Test
    @Rollback
    public void testSample() {

        // 动态检索
        TableInfoDto condition = new TableInfoDto();
        condition.setTableName("FIREEMBLEM_HERO");
        condition.setColFifterable("1");

        int searchCount = testRepository.getCountByDto(condition);
        List<TableInfo> resultList = testRepository.selectByDto(condition);
        Assert.assertTrue(resultList.size() == searchCount);

    }

    @Test
    public void testJdbcTemplate(){
        String query = "SELECT DISTINCT NAME_CN,NAME,NAME_JP FROM FIREEMBLEM_HERO WHERE NAME = ?";
        List<Object[]> queryResult = jdbcTemplate.query(query, new Object[]{"Lyn"}, new RowMapper<Object[]>() {
            @Override
            public Object[] mapRow(ResultSet rs, int rowNum) throws SQLException {
                return new Object[]{
                        rs.getString("NAME_CN"),
                        rs.getString("NAME"),
                        rs.getString("NAME_JP")
                };
            }
        });
        for(Object[] row: queryResult) {
            //String[] columns = (String[]) row;
            System.out.println(row[0] + ";" + row[1] + ";" + row[2]);
        }
    }
}
