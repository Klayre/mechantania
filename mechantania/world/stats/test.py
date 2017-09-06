import mech_base_stats

mbh = mech_base_stats.MechBaseStatContainer({"rar":10})


print(mbh.get("rar"))
mbh.add("rar", value=11)
print(mbh.get("rar"))
mbh.set("rar", value=12)
print(mbh.get("rar"))

mds = mbh.get_stats_data_object("rar")
print(mds)

mbh.delete("rar")

print(mds)

mbh.set("rar", value=13)
print(mbh.get("rar"))

mbh.add("rar", value=9)
mds2 = mech_base_stats.MechStatData("rar2", 222)
mbh.add_stats_data_object(mds2)

print(mbh.stats_data)

#
#print(mbh.get_value(t))



#mbh2 = mech_base_stats.MechBaseStatContainer({"rar":12})
#
#mbh.add_other_stats_container(mbh2)
#mbh.add_other_stats_container(mbh2)
#
#print(mbh.get_value("rar", combined=True))
