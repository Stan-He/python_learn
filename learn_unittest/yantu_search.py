#coding:UTF-8
import urllib
from urlparse import urlparse       #url解析函数
from urlparse import parse_qs
import BaseTestTool                 #自定义的工具模块
import unittest
from lxml import  etree

class YantuSearchTestClass(unittest.TestCase):
    """
            沿途搜索测试用例
    """
    #创建需要使用到的工具类对象
    tool=BaseTestTool.BaseTestTool()
    
    
    #沿途搜索请求url
    sample_url="http://10.2.39.120:2099/bin/sp?data_type=POI&query_type=line_around&keywords=&city=&category=200300&user_loc=&geoline=116.370792;40.001583;116.372655;40.001642;116.374517;40.001701;116.37638;40.00176;116.378242;40.00182;116.380105;40.001879;116.381967;40.001938;116.38383;40.001997;116.385692;40.002056;116.387555;40.002115;116.389418;40.002175;116.39128;40.002234;116.393143;40.002293;116.395005;40.002352;116.396868;40.002411;116.39873;40.00247;116.400593;40.00253;116.402456;40.002589;116.404318;40.002648;116.406181;40.002707;116.408043;40.002766;116.409906;40.002825;116.411768;40.002885;116.413631;40.002944;116.415493;40.003003&use_log=false&query_src=test&user_info=test&qii=true&show_uuid=true&show_task_code=true&citysuggestion=true&addr_poi_merge=true&need_expand_range=true&page_num=10&page=1&show_fields=all"
    paradict=tool.urlParse(sample_url)

    
    def setUp(self):
        self.url = self.createUrlPrefix('10.2.39.120','2099')
    def tearDown(self):
        pass
    
    def createUrlPrefix(self,ip,port):
        #http://10.2.39.120:2099/bin/sp?
        strTmp = 'http://'+ip+':'+port+'/bin/sp?'
        return strTmp
    
    def test_200300(self):
        """
                        测试长安街5km的沿途搜卫生间
        """
        #category=卫生间
        self.paradict['category'] = '200300'
        #geoline设置为长安街
        self.paradict['geoline']=self.tool.produceGeoline(116.374601,39.907111,116.436174,39.908461)
        params = urllib.urlencode(self.paradict)
        weburl = "%s%s"%(self.url,params)
        f = urllib.urlopen(weburl)
        #解析结果
        root=etree.fromstring(f.read())
        #断言，长安街上存在超过20个卫生间
        poi_list=root.xpath('KeywordRes/list/searchresult/list//poi')
        #print len(poi_list)
        self.assertGreater(len(poi_list), 10)
        self.assertLess(len(poi_list), 20)
        #断言，结果经纬度在geoline范围内
        for poi in poi_list:
            for x in poi.xpath('./x'):
                #print x.text,
                self.assertGreater(float(x.text), 116.368, msg="卫生间经度小于116.368")
                self.assertLess(float(x.text), 116.441, msg="卫生间经度大于116.441")
            for y in poi.xpath('./y'):
                #print y.text
                self.assertGreater(float(y.text), 39.900, msg="卫生间纬度超过范围")
                self.assertLess(float(y.text), 39.9136, msg="卫生间纬度超过范围")
        
    def test_160300(self):
        """
                         测试大屯路附近的银行，主要测试分类是否正确
        """
        #设置类别为工商银行和招商银行<typecode>160302</typecode>
        self.paradict['category'] = '160302|160306'
        #geoline为大屯路
        self.paradict['geoline']=self.tool.produceGeoline(116.370792,40.001583,116.417356,40.003062)
        params = urllib.urlencode(self.paradict)
        weburl = "%s%s"%(self.url,params)
        f = urllib.urlopen(weburl)
        #解析结果
        root=etree.fromstring(f.read())
        poi_list=root.xpath('KeywordRes/list/searchresult/list//poi')
        for poi in poi_list:
            for type_code in poi.xpath('./typecode'):
                #print type_code.text
                #断言，返回的typecode为工行或招行
                self.assertIn(type_code.text, ["160302","160306"], msg="返回的poi类型不是招行或者工行")
    
    def test_010100(self):
        """
                         测试上海周家嘴路附近的加油站，主要测试分类是否正确
        """
        #设置类别为中石化、中石油<typecode>160302</typecode>
        self.paradict['category'] = '010102|010101'
        #geoline为上海周家嘴路
        self.paradict['geoline']=self.tool.produceGeoline(121.508446,31.262705,121.555309,31.286766)
        params = urllib.urlencode(self.paradict)
        weburl = "%s%s"%(self.url,params)
        f = urllib.urlopen(weburl)
        #解析结果
        root=etree.fromstring(f.read())
        poi_list=root.xpath('KeywordRes/list/searchresult/list//poi')
        for poi in poi_list:
            for type_code in poi.xpath('./typecode'):
                #print type_code.text
                #断言，返回的typecode为中石油或中石化加油站
                self.assertIn(type_code.text, ["010102","010101"], msg="返回的poi类型不是中石油或中石化加油站")
            
    def test_030000(self):
        """
                         测试沪蓉高速，仙人山休息区的维修厂，主要测试在一段长距离的道路上，是否返回正确
        """
        #设置类别为汽车维修
        self.paradict['category'] = '030000'
        #geoline为沪蓉高速仙人山休息区附近
        self.paradict['geoline']=self.tool.produceGeoline(119.254782,32.037694,119.414005,32.049843)
        params = urllib.urlencode(self.paradict)
        weburl = "%s%s"%(self.url,params)
        f = urllib.urlopen(weburl)
        #解析结果
        root=etree.fromstring(f.read())
        poi_list=root.xpath('KeywordRes/list/searchresult/list//poi')
        #print len(poi_list)
        for poi in poi_list:
            for type_code in poi.xpath('./typecode'):
                #print type_code.text[0:3]
                #断言，返回的typecode为汽车维修
                self.assertEqual(type_code.text[0:3], "030", msg="返回的poi类型不是汽车维修")

    def test_160300_real(self):
        """
        测试方恒国际中心--炎黄艺术馆的真实case
        """
        self.paradict['category'] = '010100'
        #geoline为大屯路
        #self.paradict['geoline']='116.48129805922511;39.98962285644488;116.4808501303196;39.98916150659293;116.4808461111111;39.98915777777778;116.47474861111111;39.993180833333334;116.47253583333334;39.99462111111111;116.47237833333334;39.9946875;116.47071166666667;39.99317722222222;116.47070722222222;39.9931725;116.46812666666666;39.997186666666664'
        #geoline为东四环北路/bin/sp?query_type=line_around&data_type=POI&qii=true&show_fields=all&category=160300&geoline=116.48116797208786%3B39.98948517106915%3B116.48085147142412%3B39.98916150659293%3B116.4808461111111%3B39.98915777777778%3B116.47985222222222%3B39.9898175%3B116.47964388888889%3B39.98984361111111%3B116.47757833333333%3B39.98800388888889%3B116.47760416666667%3B39.987699444444445%3B116.48226%3B39.98453694444444%3B116.48258527777777%3B39.9843375%3B116.48258666666666%3B39.98433138888889%3B116.47809055555555%3B39.980269444444446%3B116.47431555555555%3B39.976820277777776%3B116.46972833333334%3B39.972685%3B116.46828777777777%3B39.971405
        self.paradict['geoline']='116.48116797208786;39.98948517106915;116.48085147142412;39.98916150659293;116.4808461111111;39.98915777777778;116.47985222222222;39.9898175;116.47964388888889;39.98984361111111;116.47757833333333;39.98800388888889;116.47760416666667;39.987699444444445;116.48226;39.98453694444444;116.48258527777777;39.9843375;116.48258666666666;39.98433138888889;116.47809055555555;39.980269444444446;116.47431555555555;39.976820277777776;116.46972833333334;39.972685;116.46828777777777;39.971405'
        #geoline为大山子加油站
        self.paradict['geoline']='116.48116797208786;39.98948517106915;116.48085147142412;39.98916150659293;116.4808461111111;39.98915777777778;116.47985222222222;39.9898175;116.47984805555555;39.9898175;116.48270333333333;39.99245166666667;116.48270388888889;39.99245222222222;116.4878375;39.989068055555556;116.48946833333333;39.98795333333333;116.48947027777778;39.987946944444445;116.48962138888889;39.98231861111111;116.48969027777778;39.976954722222224;116.48973305555556;39.97126111111111;116.48976333333333;39.970080555555555'
        params = urllib.urlencode(self.paradict)
        weburl = "%s%s"%(self.url,params)
        print weburl
        f = urllib.urlopen(weburl)
        #解析结果
        root=etree.fromstring(f.read())
        poi_list=root.xpath('KeywordRes/list/searchresult/list//poi')
        print len(poi_list)


if __name__ == '__main__':
    unittest.main()
        
