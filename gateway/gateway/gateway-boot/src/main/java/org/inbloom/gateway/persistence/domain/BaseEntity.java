package org.inbloom.gateway.persistence.domain;

import javax.persistence.Column;
import javax.persistence.MappedSuperclass;
import java.util.Date;

/**
 * Created by lloydengebretsen on 2/15/14.
 */
@MappedSuperclass
public abstract class BaseEntity {

    @Column
    private Date createdAt;
    @Column
    private String createdBy;
    @Column
    private Date updatedAt;
    @Column
    private String updatedBy;


    public BaseEntity(String createdBy){
        this.createdBy = createdBy;
        this.createdAt = new Date();
    }

    public BaseEntity()
    {
        super();
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    public String getCreatedBy() {
        return createdBy;
    }

    public void setCreatedBy(String createdBy) {
        this.createdBy = createdBy;
    }

    public Date getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(Date updatedAt) {
        this.updatedAt = updatedAt;
    }

    public String getUpdatedBy() {
        return updatedBy;
    }

    public void setUpdatedBy(String updatedBy) {
        this.updatedBy = updatedBy;
    }

}
