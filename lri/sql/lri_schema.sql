SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';


-- -----------------------------------------------------
-- Table `FRAMEWORKS`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `FRAMEWORKS` (
  `ID` INT NOT NULL ,
  `NAME` VARCHAR(255) NOT NULL ,
  `URL` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`ID`) ,
  UNIQUE INDEX `NAME_UNIQUE` (`NAME` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `STANDARDS`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STANDARDS` (
  `ID` INT NOT NULL ,
  `EXTERNAL_ID` VARCHAR(255) NULL ,
  `FRAMEWORK_ID` INT NOT NULL ,
  `PARENT_ID` INT NULL ,
  `HEADING` VARCHAR(255) NULL ,
  `SUBHEADING` VARCHAR(255) NULL ,
  `STANDARD_TEXT` VARCHAR(255) NULL ,
  INDEX `fk_Frameworks_ID_idx` (`FRAMEWORK_ID` ASC) ,
  PRIMARY KEY (`ID`) ,
  CONSTRAINT `fk_StandardsToFrameworks_ID_idx`
    FOREIGN KEY (`FRAMEWORK_ID` )
    REFERENCES `FRAMEWORKS` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `INTERACTIVITY`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `INTERACTIVITY` (
  `ID` INT NOT NULL ,
  `NAME` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RESOURCES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `RESOURCES` (
  `ID` INT NOT NULL ,
  `EXTERNAL_GUID` CHAR(36) NOT NULL ,
  `NAME` VARCHAR(255) NOT NULL ,
  `URL` VARCHAR(255) NULL ,
  `DESCRIPTION` VARCHAR(255) NULL ,
  `COPYRIGHT_YEAR` VARCHAR(10) NULL ,
  `USE_RIGHTS_URL` VARCHAR(255) NULL ,
  `IS_BASED_ON_URL` VARCHAR(255) NULL ,
  `TIME_REQUIRED` VARCHAR(255) NULL ,
  `INTERACTIVITY_ID` INT NULL ,
  `DATE_CREATED` DATETIME NULL ,
  `DATE_MODIFIED` DATETIME NULL ,
  `DATE_INSERTED` DATETIME NULL ,
  `DATE_UPDATED` DATETIME NULL ,
  PRIMARY KEY (`ID`) ,
  UNIQUE INDEX `external_GUID_UNIQUE` (`EXTERNAL_GUID` ASC) ,
  INDEX `fk_ResourceToInteractivity_idx_idx` (`INTERACTIVITY_ID` ASC) ,
  CONSTRAINT `fk_ResourceToInteractivity_idx`
    FOREIGN KEY (`INTERACTIVITY_ID` )
    REFERENCES `INTERACTIVITY` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ALIGNMENTS`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ALIGNMENTS` (
  `ID` INT NOT NULL ,
  `NAME` VARCHAR(255) NOT NULL COMMENT 'Aligns to LRMI type EducationalUse' ,
  PRIMARY KEY (`ID`) ,
  UNIQUE INDEX `NAME_UNIQUE` (`NAME` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `STANDARD_RESOURCES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `STANDARD_RESOURCES` (
  `ID` INT NOT NULL ,
  `STANDARD_ID` INT NOT NULL ,
  `RESOURCE_ID` INT NOT NULL ,
  `ALIGNMENT_ID` INT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_ResourceForStandard_Standard_idx` (`RESOURCE_ID` ASC) ,
  INDEX `fk_ResourceForStandard_Standard_idx_idx` (`STANDARD_ID` ASC) ,
  INDEX `fk_ResourceStandardForAlignment_Alignment_idx_idx` (`ALIGNMENT_ID` ASC) ,
  CONSTRAINT `fk_ResourceForStandard_Resource_idx`
    FOREIGN KEY (`RESOURCE_ID` )
    REFERENCES `RESOURCES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ResourceForStandard_Standard_idx`
    FOREIGN KEY (`STANDARD_ID` )
    REFERENCES `STANDARDS` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ResourceStandardForAlignment_Alignment_idx`
    FOREIGN KEY (`ALIGNMENT_ID` )
    REFERENCES `ALIGNMENTS` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PATHWAYS`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `PATHWAYS` (
  `ID` INT NOT NULL ,
  `NAME` VARCHAR(255) NOT NULL ,
  `EXTERNAL_ID` VARCHAR(255) NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PATHWAY_STANDARDS`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `PATHWAY_STANDARDS` (
  `ID` INT NOT NULL ,
  `STANDARD_ID` INT NOT NULL ,
  `PATHWAY_ID` INT NOT NULL ,
  `PRIOR_STEP_ID` INT NULL ,
  `NEXT_STEP_ID` INT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_PathwayStandard_PathwayStandard1_idx` (`PRIOR_STEP_ID` ASC) ,
  INDEX `fk_PathwayStandard_PathwayStandard2_idx` (`NEXT_STEP_ID` ASC) ,
  INDEX `fk_PathwayStandard_Standard_idx_idx` (`STANDARD_ID` ASC) ,
  INDEX `fk_PathwayStandard_Pathway_idx_idx` (`PATHWAY_ID` ASC) ,
  CONSTRAINT `fk_PathwayStandard_PathwayStandard1`
    FOREIGN KEY (`PRIOR_STEP_ID` )
    REFERENCES `PATHWAY_STANDARDS` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PathwayStandard_PathwayStandard2`
    FOREIGN KEY (`NEXT_STEP_ID` )
    REFERENCES `PATHWAY_STANDARDS` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PathwayStandard_Standard_idx`
    FOREIGN KEY (`STANDARD_ID` )
    REFERENCES `STANDARDS` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PathwayStandard_Pathway_idx`
    FOREIGN KEY (`PATHWAY_ID` )
    REFERENCES `PATHWAYS` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AUDIENCES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `AUDIENCES` (
  `ID` INT NOT NULL COMMENT '		' ,
  `NAME` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`ID`) ,
  UNIQUE INDEX `NAME_UNIQUE` (`NAME` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TAGS`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `TAGS` (
  `ID` INT NOT NULL ,
  `NAME` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`ID`) ,
  UNIQUE INDEX `NAME_UNIQUE` (`NAME` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RESOURCE_AUDIENCES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `RESOURCE_AUDIENCES` (
  `ID` INT NOT NULL COMMENT '		' ,
  `RESOURCE_ID` INT NOT NULL ,
  `AUDIENCE_ID` INT NOT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_AudiencesForResources_Resource_idx_idx` (`RESOURCE_ID` ASC) ,
  INDEX `fk_AudiencesForResources_Audiences_idx_idx` (`AUDIENCE_ID` ASC) ,
  CONSTRAINT `fk_AudiencesForResources_Resource_idx`
    FOREIGN KEY (`RESOURCE_ID` )
    REFERENCES `RESOURCES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_AudiencesForResources_Audiences_idx`
    FOREIGN KEY (`AUDIENCE_ID` )
    REFERENCES `AUDIENCES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RESOURCE_TAGS`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `RESOURCE_TAGS` (
  `ID` INT NOT NULL ,
  `RESOURCE_ID` INT NOT NULL ,
  `TAG_ID` INT NOT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_TagsForResources_Tag_idx_idx` (`TAG_ID` ASC) ,
  INDEX `fk_TagsForResources_Resource_idx_idx` (`RESOURCE_ID` ASC) ,
  CONSTRAINT `fk_TagsForResources_Tag_idx`
    FOREIGN KEY (`TAG_ID` )
    REFERENCES `TAGS` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_TagsForResources_Resource_idx`
    FOREIGN KEY (`RESOURCE_ID` )
    REFERENCES `RESOURCES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PARTIES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `PARTIES` (
  `ID` INT NOT NULL COMMENT '	' ,
  `NAME` VARCHAR(255) NOT NULL ,
  `URL` VARCHAR(255) NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PARTY_TYPES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `PARTY_TYPES` (
  `ID` INT NOT NULL ,
  `NAME` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RESOURCE_PARTIES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `RESOURCE_PARTIES` (
  `ID` INT NOT NULL ,
  `RESOURCE_ID` INT NOT NULL COMMENT '	' ,
  `PARTY_ID` INT NOT NULL ,
  `PARTY_TYPE_ID` INT NOT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_ResourcesToParties_Resource_idx_idx` (`RESOURCE_ID` ASC) ,
  INDEX `fk_ResourcesToParties_Party_idx_idx` (`PARTY_ID` ASC) ,
  INDEX `fk_ResourcesToPartyTypes_PartyType_idx_idx` (`PARTY_TYPE_ID` ASC) ,
  CONSTRAINT `fk_ResourcesToParties_Resource_idx`
    FOREIGN KEY (`RESOURCE_ID` )
    REFERENCES `RESOURCES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ResourcesToParties_Party_idx`
    FOREIGN KEY (`PARTY_ID` )
    REFERENCES `PARTIES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ResourcesToPartyTypes_PartyType_idx`
    FOREIGN KEY (`PARTY_TYPE_ID` )
    REFERENCES `PARTY_TYPES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LANGUAGES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `LANGUAGES` (
  `ID` INT NOT NULL ,
  `NAME` VARCHAR(255) NOT NULL ,
  `CODE` VARCHAR(40) NOT NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RESOURCE_LANGUAGES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `RESOURCE_LANGUAGES` (
  `ID` INT NOT NULL COMMENT '	' ,
  `RESOURCE_ID` INT NOT NULL ,
  `LANGUAGE_ID` INT NOT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_ResourcesToLanguages_Resource_idx_idx` (`RESOURCE_ID` ASC) ,
  INDEX `fk_ResourcesToLanguages_Language_idx_idx` (`LANGUAGE_ID` ASC) ,
  CONSTRAINT `fk_ResourcesToLanguages_Resource_idx`
    FOREIGN KEY (`RESOURCE_ID` )
    REFERENCES `RESOURCES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ResourcesToLanguages_Language_idx`
    FOREIGN KEY (`LANGUAGE_ID` )
    REFERENCES `LANGUAGES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `USES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `USES` (
  `ID` INT NOT NULL ,
  `NAME` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RESOURCE_USES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `RESOURCE_USES` (
  `ID` INT NOT NULL ,
  `RESOURCE_ID` INT NOT NULL ,
  `USE_ID` INT NOT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_ResourcesToUses_Resource_idx_idx` (`RESOURCE_ID` ASC) ,
  INDEX `fk_ResourcesToUses_Use_idx_idx` (`USE_ID` ASC) ,
  CONSTRAINT `fk_ResourcesToUses_Resource_idx`
    FOREIGN KEY (`RESOURCE_ID` )
    REFERENCES `RESOURCES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ResourcesToUses_Use_idx`
    FOREIGN KEY (`USE_ID` )
    REFERENCES `USES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ACTIVITY`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ACTIVITY` (
  `ID` INT NOT NULL ,
  `RESOURCE_ID` INT NOT NULL ,
  `ACTOR` VARCHAR(255) NOT NULL COMMENT '	' ,
  `VERB` VARCHAR(255) NOT NULL ,
  `VALUE` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_ActivitiesToResources_Resource_idx_idx` (`RESOURCE_ID` ASC) ,
  CONSTRAINT `fk_ActivitiesToResources_Resource_idx`
    FOREIGN KEY (`RESOURCE_ID` )
    REFERENCES `RESOURCES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AGERANGES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `AGERANGES` (
  `ID` INT NOT NULL ,
  `NAME` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RESOURCE_AGERANGES`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `RESOURCE_AGERANGES` (
  `ID` INT NOT NULL ,
  `RESOURCE_ID` INT NOT NULL COMMENT '	' ,
  `AGERANGE_ID` INT NOT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_ResourceToAgeRange_Standard_idx_idx` (`RESOURCE_ID` ASC) ,
  INDEX `fk_ResourceToAgeRange_AgeRange_idx_idx` (`AGERANGE_ID` ASC) ,
  CONSTRAINT `fk_ResourceToAgeRange_Resource_idx`
    FOREIGN KEY (`RESOURCE_ID` )
    REFERENCES `RESOURCES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ResourceToAgeRange_AgeRange_idx`
    FOREIGN KEY (`AGERANGE_ID` )
    REFERENCES `AGERANGES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TIMEREQUIRED`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `TIMEREQUIRED` (
  `ID` INT NOT NULL COMMENT '		' ,
  `NAME` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`ID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RESOURCE_TIMEREQUIREDS`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `RESOURCE_TIMEREQUIREDS` (
  `ID` INT NOT NULL COMMENT '	' ,
  `RESOURCE_ID` INT NOT NULL ,
  `TIMEREQUIRED_ID` INT NOT NULL ,
  PRIMARY KEY (`ID`) ,
  INDEX `fk_ResourcesToTimeRequireds_Resource_idx_idx` (`RESOURCE_ID` ASC) ,
  INDEX `fk_ResourcesToTimeRequireds_TimeRequired_idx_idx` (`TIMEREQUIRED_ID` ASC) ,
  CONSTRAINT `fk_ResourcesToTimeRequireds_TimeRequired_idx`
    FOREIGN KEY (`TIMEREQUIRED_ID` )
    REFERENCES `TIMEREQUIRED` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ResourcesToTimeRequireds_Resource_idx`
    FOREIGN KEY (`RESOURCE_ID` )
    REFERENCES `RESOURCES` (`ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
