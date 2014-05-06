package org.inbloom.gateway.configuration;

import org.inbloom.gateway.util.mapper.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.support.ConversionServiceFactoryBean;
import org.springframework.core.convert.ConversionService;
import org.springframework.core.convert.converter.Converter;

import java.util.HashSet;
import java.util.Set;

/**
 * Created by lloydengebretsen on 3/7/14.
 */
@Configuration
public class ConversionConfiguration {

    @Bean
    public ConversionService conversionService() {
        ConversionServiceFactoryBean bean = new ConversionServiceFactoryBean();
        bean.setConverters(getConverters());
        bean.afterPropertiesSet();
        return bean.getObject();
    }

    private Set<Converter> getConverters() {
        Set<Converter> converters = new HashSet<Converter>();

        converters.add(new DomainOperatorModelMapper());
        converters.add(new PersistentOperatorModelMapper());
        converters.add(new DomainApplicationProviderModelMapper());
        converters.add(new PersistentApplicationProviderModelMapper());
        converters.add(new DomainUserModelMapper());
        converters.add(new PersistentUserModelMapper());
        converters.add(new PersistentVerificationModelMapper());
        converters.add(new DomainVerificationModelMapper());

        return converters;
    }
}

