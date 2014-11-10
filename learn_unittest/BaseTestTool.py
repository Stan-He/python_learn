#coding:UTF-8

import math
import urlparse      #url解析函数
from lxml import etree
class BaseTestTool():
    """
            编写测试case时会使用到的通用工具类
    """
    
    def disCalc(self,lng1,lat1,lng2,lat2):
        """
                        根据输入的两个坐标点，计算距离，返回距离s（公里）
                        调用方法dis_calc(116.370792,40.001583,116.417356,40.003062)
        """
        #地球半径
        EARTH_RADIUS = 6378.137
        #切换弧度
        rad= lambda x:x*math.pi/180.0
        radLat1=rad(lat1)
        radLat2=rad(lat2)
        a = radLat1-radLat2
        b = rad(lng1)-rad(lng2)
        
        s=2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radLat1)*math.cos(radLat2)*math.pow(math.sin(b/2), 2)))
        s=s*EARTH_RADIUS
        s=round(s,4)
        return s
    
    def produceGeoline(self,lng1,lat1,lng2,lat2):
        """
                        沿途搜索，制造geoline函数，输入两个经纬度坐标，返回一组以这两个经纬度坐标做起终点的字符串，一共包含25个经纬度坐标，5公里范围
                        使用方法 produce_geoline(116.370792,40.001583,116.417356,40.003062)
        """
        distance_x=(lng2-lng1)/24
        distance_y=(lat2-lat1)/24
        geoline=str(lng1)+";"+str(lat1)
        new_x=lng1
        new_y=lat1
        for i in range(24):
            new_x=new_x+distance_x
            new_y=new_y+distance_y
            geoline+=";"+str(round(new_x,6))+";"+str(round(new_y,6))
        
        return geoline
        
    def urlParse(self,url):
        """
                        解析一个url，返回一个参数字典
        """
        #使用urlparse函数
        o=urlparse.urlparse(url)
        #参数字符串
        s1=o.query
        #print s1
        pairs=[s2.split('=') for s2 in [s1 for s1 in s1.split('&')]]

        dict={}
        for i in pairs:
            dict[i[0]]=i[1]
        return dict
 
        
        
if __name__ == '__main__':
    
    t=BaseTestTool()
    dis=t.disCalc(116.370792,40.001583,116.417356,40.003062)
    print dis
    dis2=t.disCalc(121.550674,31.209939,121.562777,31.211333)
    print dis2
    print t.produceGeoline(116.370792,40.001583,116.417356,40.003062)
    print "-----------"
    
    from urlparse import parse_qs
    sample_url="http://10.2.39.120:2099/bin/sp?data_type=POI&query_type=line_around&keywords=&city=&category=200300&user_loc=&geoline=116.370792;40.001583;116.372655;40.001642;116.374517;40.001701;116.37638;40.00176;116.378242;40.00182;116.380105;40.001879;116.381967;40.001938;116.38383;40.001997;116.385692;40.002056;116.387555;40.002115;116.389418;40.002175;116.39128;40.002234;116.393143;40.002293;116.395005;40.002352;116.396868;40.002411;116.39873;40.00247;116.400593;40.00253;116.402456;40.002589;116.404318;40.002648;116.406181;40.002707;116.408043;40.002766;116.409906;40.002825;116.411768;40.002885;116.413631;40.002944;116.415493;40.003003&use_log=false&query_src=test&user_info=test&qii=true&show_uuid=true&show_task_code=true&citysuggestion=true&addr_poi_merge=true&need_expand_range=true&page_num=10&page=1&show_fields=all"
    print t.urlParse(sample_url)
    
    