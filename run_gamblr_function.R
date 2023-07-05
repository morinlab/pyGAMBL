#!/usr/bin/env Rscript
## the line below is only needed for a Mac installation
#!/usr/local/bin/Rscript
library(argparse)
library(readr)
library(GAMBLR)

parser <- ArgumentParser(description= 'This progrom runs a GAMBLR function with arguments specified with --args argname=argvalue')

parser$add_argument('--function_name', '-f', help= 'A valid GAMBLR function name')
parser$add_argument('--args', '-a', help= 'One or more arguments in format argname=argvalue', type= 'character',   nargs='+')

xargs<- parser$parse_args()

FUNCTION <- xargs$function_name
ARGS <- xargs$args #argname = argvalue

get_args = function(all_args){
    arg_split = list()
    for(arg in all_args){
        pieces = unlist(strsplit(arg,"="))
        arg_split[[pieces[1]]]=pieces[2]
    }
    return(arg_split)
}
arglist = get_args(ARGS)

available_args = names(formals(FUNCTION))

#check if our function handles the parameters given
if(any(! names(arglist) %in% available_args)){
    bad_arg = names(arglist)[which(!names(arglist) %in% available_args)]
    stop(paste("ERROR:",bad_arg,"not in available arguments for",FUNCTION))
}

message(paste("FUNCTION:",FUNCTION))
message(paste("ARGS:",arglist))

output = do.call(FUNCTION,arglist)

cat(format_tsv(output))
