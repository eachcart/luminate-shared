#primary-static-config

? ::    ██╗     ██╗   ██╗███╗   ███╗██╗███╗   ██╗ █████╗ ████████╗███████╗  ::
? ::    ██║     ██║   ██║████╗ ████║██║████╗  ██║██╔══██╗╚══██╔══╝██╔════╝  ::
? ::    ██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║███████║   ██║   █████╗    ::
? ::    ██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██╔══██║   ██║   ██╔══╝    ::
? ::    ███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║  ██║   ██║   ███████╗  ::
? ::    ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚══════╝  ::

luminate :: {
    version :: "1.0.0"
    branch :: "stable, shared"
    build :: "Luminate"
    framework :: "PyroGram"
    prefix :: "?"
    image_path :: "Resources/Misc/images/luminate.png"
    image_path_small :: "Resources/Misc/images/luminate_small.png"
    info_path :: "Resources/Misc/info/luminate.info"

    credentials :: {
        api_id :: null ? :: paste your api_id here
        api_hash :: null ? :: paste your api_hash here with ""
        session :: "lumi"
        bot_token :: null ? :: not needed
    }
}

misc :: {
    current :: "luminate"
    website :: "https://userlumi.ru/"
    milenium :: "https://raw.githubusercontent.com/eachcart/luminate/refs/heads/main/repo.json"
    asb_sleep_min :: 0.5
    asb_sleep_max :: 1
}
