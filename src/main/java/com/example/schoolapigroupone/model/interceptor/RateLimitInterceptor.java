package com.example.schoolapigroupone.model.interceptor;

import com.example.schoolapigroupone.model.exception.TooManyRequestException;
import lombok.Getter;
import lombok.Setter;
import org.springframework.http.converter.json.GsonBuilderUtils;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@Component
public class RateLimitInterceptor implements HandlerInterceptor {

    private static final int TOO_MANY_REQUESTS_MAX_REQUESTS = 2;
    @Getter @Setter
    private int requestCount = 0;


    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        if (requestCount == TOO_MANY_REQUESTS_MAX_REQUESTS) {
            requestCount = 0;
            throw new TooManyRequestException();
        }else{
            requestCount++;
            return true;
        }
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {

    }
}
