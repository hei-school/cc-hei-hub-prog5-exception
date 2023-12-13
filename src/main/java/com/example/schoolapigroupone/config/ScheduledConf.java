package com.example.schoolapigroupone.config;

import com.example.schoolapigroupone.model.interceptor.RateLimitInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;

@Configuration
@EnableScheduling
public class ScheduledConf {
    private final RateLimitInterceptor rateLimitInterceptor;

    public ScheduledConf(RateLimitInterceptor rateLimitInterceptor) {
        this.rateLimitInterceptor = rateLimitInterceptor;
    }

    @Scheduled(fixedRate = 2000)
    public void executeTask() {
        rateLimitInterceptor.setRequestCount(0);
    }
}
