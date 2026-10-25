# Single source of truth for the reference list (used by the paper, the study guide and the checks).
# Every entry with a DOI was checked against Crossref (build/verify_refs.py, build/cr_search.py).
REFS = [
 # 1
 ("DasGupta, S., & Ganguly, S. Microscale Transport Processes, Lectures 1-4 (course notes: Lecture 1; Lecture 2 - Top-Down Approach; Lecture 3 - Bottom-Up Approach; Lecture 4 - Main Issues of Successful Microstructures). IIT Kharagpur.", None),
 # 2
 ("Bhat, G., Gumussoy, S., & Ogras, U. Y. (2019). Power and thermal analysis of commercial mobile platforms: Experiments and case studies. Proc. Design, Automation & Test in Europe (DATE) 2019, 144-149.", "https://doi.org/10.23919/DATE.2019.8714831"),
 # 3
 ("Garimella, S. V., Fleischer, A. S., Murthy, J. Y., Keshavarzi, A., Prasher, R., Patel, C., ... Raad, P. (2008). Thermal challenges in next-generation electronic systems. IEEE Trans. Components and Packaging Technologies, 31(4), 801-815.", "https://doi.org/10.1109/TCAPT.2008.2001197"),
 # 4
 ("Tuckerman, D. B., & Pease, R. F. W. (1981). High-performance heat sinking for VLSI. IEEE Electron Device Letters, 2(5), 126-129.", "https://doi.org/10.1109/EDL.1981.25367"),
 # 5
 ("Faghri, A. (2012). Review and advances in heat pipe science and technology. Journal of Heat Transfer, 134(12), 123001.", "https://doi.org/10.1115/1.4007407"),
 # 6
 ("Peterson, G. P., & Ma, H. B. (1996). Theoretical analysis of the maximum heat transport in triangular grooves: A study of idealized micro heat pipes. Journal of Heat Transfer, 118(3), 731-739.", "https://doi.org/10.1115/1.2822693"),
 # 7
 ("Vasiliev, L. L. (2008). Micro and miniature heat pipes - Electronic component coolers. Applied Thermal Engineering, 28(4), 266-273.", "https://doi.org/10.1016/j.applthermaleng.2006.02.023"),
 # 8
 ("Weibel, J. A., & Garimella, S. V. (2013). Recent advances in vapor chamber transport characterization for high-heat-flux applications. Advances in Heat Transfer, 45, 209-301.", "https://doi.org/10.1016/B978-0-12-407819-2.00004-9"),
 # 9
 ("Bulut, M., Kandlikar, S. G., & Sozbir, N. (2019). A review of vapor chambers. Heat Transfer Engineering, 40(19), 1551-1573.", "https://doi.org/10.1080/01457632.2018.1480868"),
 # 10
 ("Zhou, F., Zhou, J., & Huai, X. (2023). Advancements and challenges in ultra-thin vapor chambers for high-efficiency electronic thermal management: A comprehensive review. Int. J. Heat and Mass Transfer, 214, 124453.", "https://doi.org/10.1016/j.ijheatmasstransfer.2023.124453"),
 # 11
 ("Duan, L., Li, H., Du, J., Liu, K., & He, W. (2022). Research on the manufacturing process and heat transfer performance of ultra-thin heat pipes: A review. Materials, 15(15), 5459.", "https://doi.org/10.3390/ma15155459"),
 # 12
 ("Filippou, I., Tselepi, V., & Ellinas, K. (2024). A review of microfabrication approaches for the development of thin, flattened heat pipes and vapor chambers for passive electronic cooling applications. Micro and Nano Engineering, 22, 100235.", "https://doi.org/10.1016/j.mne.2023.100235"),
 # 13
 ("Hanlon, M. A., & Ma, H. B. (2003). Evaporation heat transfer in sintered porous media. Journal of Heat Transfer, 125(4), 644-652.", "https://doi.org/10.1115/1.1560145"),
 # 14
 ("Weibel, J. A., Garimella, S. V., & North, M. T. (2010). Characterization of evaporation and boiling from sintered powder wicks fed by capillary action. Int. J. Heat and Mass Transfer, 53(19-20), 4204-4215.", "https://doi.org/10.1016/j.ijheatmasstransfer.2010.05.043"),
 # 15
 ("Patankar, G., Weibel, J. A., & Garimella, S. V. (2016). Patterning the condenser-side wick in ultra-thin vapor chamber heat spreaders to improve skin temperature uniformity of mobile devices. Int. J. Heat and Mass Transfer, 101, 927-936.", "https://doi.org/10.1016/j.ijheatmasstransfer.2016.05.093"),
 # 16
 ("Yan, C., Li, H., Tang, Y., Ding, X., Yuan, X., Liang, Y., & Zhang, S. (2023). A novel ultra-thin vapor chamber with composite wick for portable electronics cooling. Applied Thermal Engineering, 226, 120340.", "https://doi.org/10.1016/j.applthermaleng.2023.120340"),
 # 17
 ("Zhang, S., Huang, H., Bai, J., Yan, C., Qiu, H., Tang, Y., & Luo, F. (2024). Experimental investigation on ultra-thin vapor chamber with composite wick for electronics thermal management. Micromachines, 15(5), 627.", "https://doi.org/10.3390/mi15050627"),
 # 18
 ("Semenic, T., & Catton, I. (2009). Experimental study of biporous wicks for high heat flux applications. Int. J. Heat and Mass Transfer, 52(21-22), 5113-5121.", "https://doi.org/10.1016/j.ijheatmasstransfer.2009.05.005"),
 # 19
 ("Khrustalev, D., & Faghri, A. (1995). Heat transfer during evaporation on capillary-grooved structures of heat pipes. Journal of Heat Transfer, 117(3), 740-747.", "https://doi.org/10.1115/1.2822638"),
 # 20
 ("Wayner, P. C., Kao, Y. K., & LaCroix, L. V. (1976). The interline heat-transfer coefficient of an evaporating wetting film. Int. J. Heat and Mass Transfer, 19(5), 487-492.", "https://doi.org/10.1016/0017-9310(76)90161-7"),
 # 21
 ("Marek, R., & Straub, J. (2001). Analysis of the evaporation coefficient and the condensation coefficient of water. Int. J. Heat and Mass Transfer, 44(1), 39-53.", "https://doi.org/10.1016/S0017-9310(00)00086-7"),
 # 22
 ("Vadakkan, U., Garimella, S. V., & Murthy, J. Y. (2004). Transport in flat heat pipes at high heat fluxes from multiple discrete sources. Journal of Heat Transfer, 126(3), 347-354.", "https://doi.org/10.1115/1.1737773"),
 # 23
 ("Ranjan, R., Murthy, J. Y., Garimella, S. V., & Vadakkan, U. (2011). A numerical model for transport in flat heat pipes considering wick microstructure effects. Int. J. Heat and Mass Transfer, 54(1-3), 153-168.", "https://doi.org/10.1016/j.ijheatmasstransfer.2010.09.057"),
 # 24
 ("Prasher, R. S. (2003). A simplified conduction based modeling scheme for design sensitivity study of thermal solution utilizing heat pipe and vapor chamber technology. Journal of Electronic Packaging, 125(3), 378-385.", "https://doi.org/10.1115/1.1602479"),
 # 25
 ("Peterson, G. P. (1994). An Introduction to Heat Pipes: Modeling, Testing, and Applications. Wiley, New York.", None),
 # 26
 ("Faghri, A. (1995). Heat Pipe Science and Technology. Taylor & Francis, Washington, DC.", None),
]
