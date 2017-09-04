import mech_base_stats

mbh = mech_base_stats.MechBaseStatContainer({"rar":10})


#print(mbh.get_value("rar"))
#
#print(mbh.get_value(t))



mbh2 = mech_base_stats.MechBaseStatContainer({"rar":12})

mbh.add_other_stats_container(mbh2)
mbh.add_other_stats_container(mbh2)

print(mbh.get_value("rar", combined=True))
