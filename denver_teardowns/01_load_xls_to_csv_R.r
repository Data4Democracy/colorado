# import .xls
# ==============================================================================
library(readxl)
library(plyr)
library(data.table)

# https://stackoverflow.com/questions/4948361/how-do-i-save-warnings-and-errors-as-output-from-a-function
# Martin Morgan
factory <- function(fun)
    function(...) {
        warn <- err <- NULL
        res <- withCallingHandlers(
            tryCatch(fun(...), error=function(e) {
                err <<- conditionMessage(e)
                NULL
            }), warning=function(w) {
                warn <<- append(warn, conditionMessage(w))
                invokeRestart("muffleWarning")
            })
        list(res, warn=warn, err=err)
    }

.has <- function(x, what)
    !sapply(lapply(x, "[[", what), is.null)
hasWarning <- function(x) .has(x, "warn")
hasError <- function(x) .has(x, "err")
isClean <- function(x) !(hasError(x) | hasWarning(x))
value <- function(x) sapply(x, "[[", 1)
cleanv <- function(x) sapply(x[isClean(x)], "[[", 1)


parseStatCodeText <- function(warning_text_entry) {
    split_up <- unlist(strsplit(warning_text_entry, "date in A| / |Code: |'"))
    split_up[c(2, 5)]
}

parsePrmtTypeText <- function(warning_text_entry) {
    split_up <- unlist(strsplit(warning_text_entry, "Permit Type: "))
    split_up[2]
}

# factory warning for read_xls
read_xls_warning <- factory(read_xls)

readCODxls <- function(file_name) {
    
    # function to read .xls
    attempted_read <- 
        read_xls_warning(file_name, skip = 2, 
                 col_types = c(
                     `Date Issued` = "date",
                     `Permit Type` = "text", "skip",
                     `Permit #` = "text", "skip", "skip",
                     `Address` = "text", "skip",
                     `Location` = "text", "skip", "skip",
                     `Class` = "text",
                     `Units` = "numeric", "skip", "skip",
                     `Valuation` = "guess",
                     `Permit Fee` = "numeric", "skip",
                     `Owner's Name` = "text", "skip",
                     `Contractor's Name` = "text", "skip"))
    
    table <- as.data.table(attempted_read[[1]])
    table[ , "Stat Code" := ""]
    table[ , "Permit Type" := ""]
    
    # fix stat codes
    stat_code_text <- attempted_read$warn[ grep("Stat Code", attempted_read$warn) ]
    
    row_and_codes <- ldply(stat_code_text, parseStatCodeText)
    row_and_codes$V1 <- as.numeric(row_and_codes$V1) - 2
    row_and_codes <- rbind(row_and_codes,
                           list(nrow(table), ""))
    
    sapply(1:(nrow(row_and_codes) - 1), function (i) {
        table[ seq(row_and_codes[i, 1], row_and_codes[i + 1, 1]),
               `Stat Code` := row_and_codes[i, 2] ]
    })
    
    # fix permit types
    permit_type_index <- grep("Permit Type: ", table$X__1)
    row_and_codes_permit <- ldply(
        table$X__1[permit_type_index], parsePrmtTypeText)
    row_and_codes_permit$permit_type_index <- permit_type_index
    row_and_codes_permit <- rbind(row_and_codes_permit, list("", nrow(table)))
    
    sapply(1:(nrow(row_and_codes_permit) - 1), function (i) {
        table[ seq(row_and_codes_permit[i, 2], row_and_codes_permit[i + 1, 2]),
               `Permit Type` := row_and_codes_permit[i, 1] ]
    })
    
    
    # final cleaning
    table <- table[!is.na(`Date Issued`) & !is.na(`Permit #`), ]
    table[ , X__1 := NULL]
    
    print(paste("read", file_name, "successfully!"))
    assign(x = gsub("\\.\\/data\\/|\\.xls", "", file_name), value = table, envir = .GlobalEnv)
}




# single case trbleshoot
# read_xls_warning(xls_filepath[13])
# readCODxls(xls_filepath[13])

xls_filepath <- list.files("./data", pattern = "*.xls", full.names = T)
sapply(xls_filepath, readCODxls)

permit_dts <- ls(pattern = "Permits*")
text = paste0("table <- rbindlist(list(`", paste(permit_dts, collapse = "`, `"), "`))")
parse(text = paste0("table <- rbindlist(list(`", paste(permit_dts, collapse = "`, `"), "`))"))
eval(parse(text = paste0("table <- rbindlist(list(`", paste(permit_dts, collapse = "`, `"), "`))")))
eval(parse(text = paste0("rm(`", paste(permit_dts, collapse = "`, `"), "`)")))

# table[ , file_name := gsub("\\.\\/data\\/", "", file_name)]
table[ , "Stat Code"]

table[ , `Permit #` := gsub("\\*failed to decode utf16\\*", "", `Permit #`)]

setorder(table, "Date Issued")
write.csv(table, file = "./output/CityOfDenverHousingPermits_XLStoCSV.csv", row.names = F)
