package com.example.mysql.controller;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

import java.nio.charset.Charset;

@RunWith(SpringRunner.class)
@SpringBootTest
@AutoConfigureMockMvc
public class ControllerTester {

    @Autowired
    private MockMvc mockMvc;

    /**
     * 表名取得情报Controller
     */
    @Test
    public void ManagementControllerTest() throws Exception {
        MvcResult result = mockMvc.perform(MockMvcRequestBuilders.get("/getFilterColumns?tableName=FIREEMBLEM_HERO"))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andReturn();

        String responseContent = result.getResponse().getContentAsString(Charset.forName("UTF-8"));
        System.out.println("响应内容：" + responseContent);

    }

}
