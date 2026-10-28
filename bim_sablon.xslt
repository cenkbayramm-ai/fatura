<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ccts="urn:un:unece:uncefact:documentation:2" xmlns:clm54217="urn:un:unece:uncefact:codelist:specification:54217:2001" xmlns:clm5639="urn:un:unece:uncefact:codelist:specification:5639:1988" xmlns:clm66411="urn:un:unece:uncefact:codelist:specification:66411:2001" xmlns:clmIANAMIMEMediaType="urn:un:unece:uncefact:codelist:specification:IANAMIMEMediaType:2003" xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:link="http://www.xbrl.org/2003/linkbase" xmlns:n1="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:qdt="urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2" xmlns:udt="urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2" xmlns:xbrldi="http://xbrl.org/2006/xbrldi" xmlns:xbrli="http://www.xbrl.org/2003/instance" xmlns:xdt="http://www.w3.org/2005/xpath-datatypes" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0" exclude-result-prefixes="cac cbc ccts clm54217 clm5639 clm66411 clmIANAMIMEMediaType fn link n1 qdt udt xbrldi xbrli xdt xlink xs xsd xsi">
<xsl:decimal-format name="european" decimal-separator="," grouping-separator="." NaN=""/>
<xsl:output version="4.0" method="html" indent="no" encoding="UTF-8" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" doctype-system="http://www.w3.org/TR/html4/loose.dtd"/>
<xsl:param name="SV_OutputFormat" select="'HTML'"/>
<xsl:variable name="XML" select="/"/>
<xsl:template match="/">
<html>
<head>
<script type="text/javascript">
<![CDATA[ var QRCode;!function(){function a(a){this.mode=c.MODE_8BIT_BYTE,this.data=a,this.parsedData=[];for(var b=[],d=0,e=this.data.length;e>d;d++){var f=this.data.charCodeAt(d);f>65536?(b[0]=240|(1835008&f)>>>18,b[1]=128|(258048&f)>>>12,b[2]=128|(4032&f)>>>6,b[3]=128|63&f):f>2048?(b[0]=224|(61440&f)>>>12,b[1]=128|(4032&f)>>>6,b[2]=128|63&f):f>128?(b[0]=192|(1984&f)>>>6,b[1]=128|63&f):b[0]=f,this.parsedData=this.parsedData.concat(b)}this.parsedData.length!=this.data.length&&(this.parsedData.unshift(191),this.parsedData.unshift(187),this.parsedData.unshift(239))}function b(a,b){this.typeNumber=a,this.errorCorrectLevel=b,this.modules=null,this.moduleCount=0,this.dataCache=null,this.dataList=[]}function i(a,b){if(void 0==a.length)throw new Error(a.length+"/"+b);for(var c=0;c<a.length&&0==a[c];)c++;this.num=new Array(a.length-c+b);for(var d=0;d<a.length-c;d++)this.num[d]=a[d+c]}function j(a,b){this.totalCount=a,this.dataCount=b}function k(){this.buffer=[],this.length=0}function m(){return"undefined"!=typeof CanvasRenderingContext2D}function n(){var a=!1,b=navigator.userAgent;return/android/i.test(b)&&(a=!0,aMat=b.toString().match(/android ([0-9]\.[0-9])/i),aMat&&aMat[1]&&(a=parseFloat(aMat[1]))),a}function r(a,b){for(var c=1,e=s(a),f=0,g=l.length;g>=f;f++){var h=0;switch(b){case d.L:h=l[f][0];break;case d.M:h=l[f][1];break;case d.Q:h=l[f][2];break;case d.H:h=l[f][3]}if(h>=e)break;c++}if(c>l.length)throw new Error("Too long data");return c}function s(a){var b=encodeURI(a).toString().replace(/\%[0-9a-fA-F]{2}/g,"a");return b.length+(b.length!=a?3:0)}a.prototype={getLength:function(){return this.parsedData.length},write:function(a){for(var b=0,c=this.parsedData.length;c>b;b++)a.put(this.parsedData[b],8)}},b.prototype={addData:function(b){var c=new a(b);this.dataList.push(c),this.dataCache=null},isDark:function(a,b){if(0>a||this.moduleCount<=a||0>b||this.moduleCount<=b)throw new Error(a+","+b);return this.modules[a][b]},getModuleCount:function(){return this.moduleCount},make:function(){this.makeImpl(!1,this.getBestMaskPattern())},makeImpl:function(a,c){this.moduleCount=4*this.typeNumber+17,this.modules=new Array(this.moduleCount);for(var d=0;d<this.moduleCount;d++){this.modules[d]=new Array(this.moduleCount);for(var e=0;e<this.moduleCount;e++)this.modules[d][e]=null}this.setupPositionProbePattern(0,0),this.setupPositionProbePattern(this.moduleCount-7,0),this.setupPositionProbePattern(0,this.moduleCount-7),this.setupPositionAdjustPattern(),this.setupTimingPattern(),this.setupTypeInfo(a,c),this.typeNumber>=7&&this.setupTypeNumber(a),null==this.dataCache&&(this.dataCache=b.createData(this.typeNumber,this.errorCorrectLevel,this.dataList)),this.mapData(this.dataCache,c)},setupPositionProbePattern:function(a,b){for(var c=-1;7>=c;c++)if(!(-1>=a+c||this.moduleCount<=a+c))for(var d=-1;7>=d;d++)-1>=b+d||this.moduleCount<=b+d||(this.modules[a+c][b+d]=c>=0&&6>=c&&(0==d||6==d)||d>=0&&6>=d&&(0==c||6==c)||c>=2&&4>=c&&d>=2&&4>=d?!0:!1)},getBestMaskPattern:function(){for(var a=0,b=0,c=0;8>c;c++){this.makeImpl(!0,c);var d=f.getLostPoint(this);(0==c||a>d)&&(a=d,b=c)}return b},createMovieClip:function(a,b,c){var d=a.createEmptyMovieClip(b,c),e=1;this.make();for(var f=0;f<this.modules.length;f++)for(var g=f*e,h=0;h<this.modules[f].length;h++){var i=h*e,j=this.modules[f][h];j&&(d.beginFill(0,100),d.moveTo(i,g),d.lineTo(i+e,g),d.lineTo(i+e,g+e),d.lineTo(i,g+e),d.endFill())}return d},setupTimingPattern:function(){for(var a=8;a<this.moduleCount-8;a++)null==this.modules[a][6]&&(this.modules[a][6]=0==a%2);for(var b=8;b<this.moduleCount-8;b++)null==this.modules[6][b]&&(this.modules[6][b]=0==b%2)},setupPositionAdjustPattern:function(){for(var a=f.getPatternPosition(this.typeNumber),b=0;b<a.length;b++)for(var c=0;c<a.length;c++){var d=a[b],e=a[c];if(null==this.modules[d][e])for(var g=-2;2>=g;g++)for(var h=-2;2>=h;h++)this.modules[d+g][e+h]=-2==g||2==g||-2==h||2==h||0==g&&0==h?!0:!1}},setupTypeNumber:function(a){for(var b=f.getBCHTypeNumber(this.typeNumber),c=0;18>c;c++){var d=!a&&1==(1&b>>c);this.modules[Math.floor(c/3)][c%3+this.moduleCount-8-3]=d}for(var c=0;18>c;c++){var d=!a&&1==(1&b>>c);this.modules[c%3+this.moduleCount-8-3][Math.floor(c/3)]=d}},setupTypeInfo:function(a,b){for(var c=this.errorCorrectLevel<<3|b,d=f.getBCHTypeInfo(c),e=0;15>e;e++){var g=!a&&1==(1&d>>e);6>e?this.modules[e][8]=g:8>e?this.modules[e+1][8]=g:this.modules[this.moduleCount-15+e][8]=g}for(var e=0;15>e;e++){var g=!a&&1==(1&d>>e);8>e?this.modules[8][this.moduleCount-e-1]=g:9>e?this.modules[8][15-e-1+1]=g:this.modules[8][15-e-1]=g}this.modules[this.moduleCount-8][8]=!a},mapData:function(a,b){for(var c=-1,d=this.moduleCount-1,e=7,g=0,h=this.moduleCount-1;h>0;h-=2)for(6==h&&h--;;){for(var i=0;2>i;i++)if(null==this.modules[d][h-i]){var j=!1;g<a.length&&(j=1==(1&a[g]>>>e));var k=f.getMask(b,d,h-i);k&&(j=!j),this.modules[d][h-i]=j,e--,-1==e&&(g++,e=7)}if(d+=c,0>d||this.moduleCount<=d){d-=c,c=-c;break}}}},b.PAD0=236,b.PAD1=17,b.createData=function(a,c,d){for(var e=j.getRSBlocks(a,c),g=new k,h=0;h<d.length;h++){var i=d[h];g.put(i.mode,4),g.put(i.getLength(),f.getLengthInBits(i.mode,a)),i.write(g)}for(var l=0,h=0;h<e.length;h++)l+=e[h].dataCount;if(g.getLengthInBits()>8*l)throw new Error("code length overflow. ("+g.getLengthInBits()+">"+8*l+")");for(g.getLengthInBits()+4<=8*l&&g.put(0,4);0!=g.getLengthInBits()%8;)g.putBit(!1);for(;;){if(g.getLengthInBits()>=8*l)break;if(g.put(b.PAD0,8),g.getLengthInBits()>=8*l)break;g.put(b.PAD1,8)}return b.createBytes(g,e)},b.createBytes=function(a,b){for(var c=0,d=0,e=0,g=new Array(b.length),h=new Array(b.length),j=0;j<b.length;j++){var k=b[j].dataCount,l=b[j].totalCount-k;d=Math.max(d,k),e=Math.max(e,l),g[j]=new Array(k);for(var m=0;m<g[j].length;m++)g[j][m]=255&a.buffer[m+c];c+=k;var n=f.getErrorCorrectPolynomial(l),o=new i(g[j],n.getLength()-1),p=o.mod(n);h[j]=new Array(n.getLength()-1);for(var m=0;m<h[j].length;m++){var q=m+p.getLength()-h[j].length;h[j][m]=q>=0?p.get(q):0}}for(var r=0,m=0;m<b.length;m++)r+=b[m].totalCount;for(var s=new Array(r),t=0,m=0;d>m;m++)for(var j=0;j<b.length;j++)m<g[j].length&&(s[t++]=g[j][m]);for(var m=0;e>m;m++)for(var j=0;j<b.length;j++)m<h[j].length&&(s[t++]=h[j][m]);return s};for(var c={MODE_NUMBER:1,MODE_ALPHA_NUM:2,MODE_8BIT_BYTE:4,MODE_KANJI:8},d={L:1,M:0,Q:3,H:2},e={PATTERN000:0,PATTERN001:1,PATTERN010:2,PATTERN011:3,PATTERN100:4,PATTERN101:5,PATTERN110:6,PATTERN111:7},f={PATTERN_POSITION_TABLE:[[],[6,18],[6,22],[6,26],[6,30],[6,34],[6,22,38],[6,24,42],[6,26,46],[6,28,50],[6,30,54],[6,32,58],[6,34,62],[6,26,46,66],[6,26,48,70],[6,26,50,74],[6,30,54,78],[6,30,56,82],[6,30,58,86],[6,34,62,90],[6,28,50,72,94],[6,26,50,74,98],[6,30,54,78,102],[6,28,54,80,106],[6,32,58,84,110],[6,30,58,86,114],[6,34,62,90,118],[6,26,50,74,98,122],[6,30,54,78,102,126],[6,26,52,78,104,130],[6,30,56,82,108,134],[6,34,60,86,112,138],[6,30,58,86,114,142],[6,34,62,90,118,146],[6,30,54,78,102,126,150],[6,24,50,76,102,128,154],[6,28,54,80,106,132,158],[6,32,58,84,110,136,162],[6,26,54,82,110,138,166],[6,30,58,86,114,142,170]],G15:1335,G18:7973,G15_MASK:21522,getBCHTypeInfo:function(a){for(var b=a<<10;f.getBCHDigit(b)-f.getBCHDigit(f.G15)>=0;)b^=f.G15<<f.getBCHDigit(b)-f.getBCHDigit(f.G15);return(a<<10|b)^f.G15_MASK},getBCHTypeNumber:function(a){for(var b=a<<12;f.getBCHDigit(b)-f.getBCHDigit(f.G18)>=0;)b^=f.G18<<f.getBCHDigit(b)-f.getBCHDigit(f.G18);return a<<12|b},getBCHDigit:function(a){for(var b=0;0!=a;)b++,a>>>=1;return b},getPatternPosition:function(a){return f.PATTERN_POSITION_TABLE[a-1]},getMask:function(a,b,c){switch(a){case e.PATTERN000:return 0==(b+c)%2;case e.PATTERN001:return 0==b%2;case e.PATTERN010:return 0==c%3;case e.PATTERN011:return 0==(b+c)%3;case e.PATTERN100:return 0==(Math.floor(b/2)+Math.floor(c/3))%2;case e.PATTERN101:return 0==b*c%2+b*c%3;case e.PATTERN110:return 0==(b*c%2+b*c%3)%2;case e.PATTERN111:return 0==(b*c%3+(b+c)%2)%2;default:throw new Error("bad maskPattern:"+a)}},getErrorCorrectPolynomial:function(a){for(var b=new i([1],0),c=0;a>c;c++)b=b.multiply(new i([1,g.gexp(c)],0));return b},getLengthInBits:function(a,b){if(b>=1&&10>b)switch(a){case c.MODE_NUMBER:return 10;case c.MODE_ALPHA_NUM:return 9;case c.MODE_8BIT_BYTE:return 8;case c.MODE_KANJI:return 8;default:throw new Error("mode:"+a)}else if(27>b)switch(a){case c.MODE_NUMBER:return 12;case c.MODE_ALPHA_NUM:return 11;case c.MODE_8BIT_BYTE:return 16;case c.MODE_KANJI:return 10;default:throw new Error("mode:"+a)}else{if(!(41>b))throw new Error("type:"+b);switch(a){case c.MODE_NUMBER:return 14;case c.MODE_ALPHA_NUM:return 13;case c.MODE_8BIT_BYTE:return 16;case c.MODE_KANJI:return 12;default:throw new Error("mode:"+a)}}},getLostPoint:function(a){for(var b=a.getModuleCount(),c=0,d=0;b>d;d++)for(var e=0;b>e;e++){for(var f=0,g=a.isDark(d,e),h=-1;1>=h;h++)if(!(0>d+h||d+h>=b))for(var i=-1;1>=i;i++)0>e+i||e+i>=b||(0!=h||0!=i)&&g==a.isDark(d+h,e+i)&&f++;f>5&&(c+=3+f-5)}for(var d=0;b-1>d;d++)for(var e=0;b-1>e;e++){var j=0;a.isDark(d,e)&&j++,a.isDark(d+1,e)&&j++,a.isDark(d,e+1)&&j++,a.isDark(d+1,e+1)&&j++,(0==j||4==j)&&(c+=3)}for(var d=0;b>d;d++)for(var e=0;b-6>e;e++)a.isDark(d,e)&&!a.isDark(d,e+1)&&a.isDark(d,e+2)&&a.isDark(d,e+3)&&a.isDark(d,e+4)&&!a.isDark(d,e+5)&&a.isDark(d,e+6)&&(c+=40);for(var e=0;b>e;e++)for(var d=0;b-6>d;d++)a.isDark(d,e)&&!a.isDark(d+1,e)&&a.isDark(d+2,e)&&a.isDark(d+3,e)&&a.isDark(d+4,e)&&!a.isDark(d+5,e)&&a.isDark(d+6,e)&&(c+=40);for(var k=0,e=0;b>e;e++)for(var d=0;b>d;d++)a.isDark(d,e)&&k++;var l=Math.abs(100*k/b/b-50)/5;return c+=10*l}},g={glog:function(a){if(1>a)throw new Error("glog("+a+")");return g.LOG_TABLE[a]},gexp:function(a){for(;0>a;)a+=255;for(;a>=256;)a-=255;return g.EXP_TABLE[a]},EXP_TABLE:new Array(256),LOG_TABLE:new Array(256)},h=0;8>h;h++)g.EXP_TABLE[h]=1<<h;for(var h=8;256>h;h++)g.EXP_TABLE[h]=g.EXP_TABLE[h-4]^g.EXP_TABLE[h-5]^g.EXP_TABLE[h-6]^g.EXP_TABLE[h-8];for(var h=0;255>h;h++)g.LOG_TABLE[g.EXP_TABLE[h]]=h;i.prototype={get:function(a){return this.num[a]},getLength:function(){return this.num.length},multiply:function(a){for(var b=new Array(this.getLength()+a.getLength()-1),c=0;c<this.getLength();c++)for(var d=0;d<a.getLength();d++)b[c+d]^=g.gexp(g.glog(this.get(c))+g.glog(a.get(d)));return new i(b,0)},mod:function(a){if(this.getLength()-a.getLength()<0)return this;for(var b=g.glog(this.get(0))-g.glog(a.get(0)),c=new Array(this.getLength()),d=0;d<this.getLength();d++)c[d]=this.get(d);for(var d=0;d<a.getLength();d++)c[d]^=g.gexp(g.glog(a.get(d))+b);return new i(c,0).mod(a)}},j.RS_BLOCK_TABLE=[[1,26,19],[1,26,16],[1,26,13],[1,26,9],[1,44,34],[1,44,28],[1,44,22],[1,44,16],[1,70,55],[1,70,44],[2,35,17],[2,35,13],[1,100,80],[2,50,32],[2,50,24],[4,25,9],[1,134,108],[2,67,43],[2,33,15,2,34,16],[2,33,11,2,34,12],[2,86,68],[4,43,27],[4,43,19],[4,43,15],[2,98,78],[4,49,31],[2,32,14,4,33,15],[4,39,13,1,40,14],[2,121,97],[2,60,38,2,61,39],[4,40,18,2,41,19],[4,40,14,2,41,15],[2,146,116],[3,58,36,2,59,37],[4,36,16,4,37,17],[4,36,12,4,37,13],[2,86,68,2,87,69],[4,69,43,1,70,44],[6,43,19,2,44,20],[6,43,15,2,44,16],[4,101,81],[1,80,50,4,81,51],[4,50,22,4,51,23],[3,36,12,8,37,13],[2,116,92,2,117,93],[6,58,36,2,59,37],[4,46,20,6,47,21],[7,42,14,4,43,15],[4,133,107],[8,59,37,1,60,38],[8,44,20,4,45,21],[12,33,11,4,34,12],[3,145,115,1,146,116],[4,64,40,5,65,41],[11,36,16,5,37,17],[11,36,12,5,37,13],[5,109,87,1,110,88],[5,65,41,5,66,42],[5,54,24,7,55,25],[11,36,12],[5,122,98,1,123,99],[7,73,45,3,74,46],[15,43,19,2,44,20],[3,45,15,13,46,16],[1,135,107,5,136,108],[10,74,46,1,75,47],[1,50,22,15,51,23],[2,42,14,17,43,15],[5,150,120,1,151,121],[9,69,43,4,70,44],[17,50,22,1,51,23],[2,42,14,19,43,15],[3,141,113,4,142,114],[3,70,44,11,71,45],[17,47,21,4,48,22],[9,39,13,16,40,14],[3,135,107,5,136,108],[3,67,41,13,68,42],[15,54,24,5,55,25],[15,43,15,10,44,16],[4,144,116,4,145,117],[17,68,42],[17,50,22,6,51,23],[19,46,16,6,47,17],[2,139,111,7,140,112],[17,74,46],[7,54,24,16,55,25],[34,37,13],[4,151,121,5,152,122],[4,75,47,14,76,48],[11,54,24,14,55,25],[16,45,15,14,46,16],[6,147,117,4,148,118],[6,73,45,14,74,46],[11,54,24,16,55,25],[30,46,16,2,47,17],[8,132,106,4,133,107],[8,75,47,13,76,48],[7,54,24,22,55,25],[22,45,15,13,46,16],[10,142,114,2,143,115],[19,74,46,4,75,47],[28,50,22,6,51,23],[33,46,16,4,47,17],[8,152,122,4,153,123],[22,73,45,3,74,46],[8,53,23,26,54,24],[12,45,15,28,46,16],[3,147,117,10,148,118],[3,73,45,23,74,46],[4,54,24,31,55,25],[11,45,15,31,46,16],[7,146,116,7,147,117],[21,73,45,7,74,46],[1,53,23,37,54,24],[19,45,15,26,46,16],[5,145,115,10,146,116],[19,75,47,10,76,48],[15,54,24,25,55,25],[23,45,15,25,46,16],[13,145,115,3,146,116],[2,74,46,29,75,47],[42,54,24,1,55,25],[23,45,15,28,46,16],[17,145,115],[10,74,46,23,75,47],[10,54,24,35,55,25],[19,45,15,35,46,16],[17,145,115,1,146,116],[14,74,46,21,75,47],[29,54,24,19,55,25],[11,45,15,46,46,16],[13,145,115,6,146,116],[14,74,46,23,75,47],[44,54,24,7,55,25],[59,46,16,1,47,17],[12,151,121,7,152,122],[12,75,47,26,76,48],[39,54,24,14,55,25],[22,45,15,41,46,16],[6,151,121,14,152,122],[6,75,47,34,76,48],[46,54,24,10,55,25],[2,45,15,64,46,16],[17,152,122,4,153,123],[29,74,46,14,75,47],[49,54,24,10,55,25],[24,45,15,46,46,16],[4,152,122,18,153,123],[13,74,46,32,75,47],[48,54,24,14,55,25],[42,45,15,32,46,16],[20,147,117,4,148,118],[40,75,47,7,76,48],[43,54,24,22,55,25],[10,45,15,67,46,16],[19,148,118,6,149,119],[18,75,47,31,76,48],[34,54,24,34,55,25],[20,45,15,61,46,16]],j.getRSBlocks=function(a,b){var c=j.getRsBlockTable(a,b);if(void 0==c)throw new Error("bad rs block @ typeNumber:"+a+"/errorCorrectLevel:"+b);for(var d=c.length/3,e=[],f=0;d>f;f++)for(var g=c[3*f+0],h=c[3*f+1],i=c[3*f+2],k=0;g>k;k++)e.push(new j(h,i));return e},j.getRsBlockTable=function(a,b){switch(b){case d.L:return j.RS_BLOCK_TABLE[4*(a-1)+0];case d.M:return j.RS_BLOCK_TABLE[4*(a-1)+1];case d.Q:return j.RS_BLOCK_TABLE[4*(a-1)+2];case d.H:return j.RS_BLOCK_TABLE[4*(a-1)+3];default:return void 0}},k.prototype={get:function(a){var b=Math.floor(a/8);return 1==(1&this.buffer[b]>>>7-a%8)},put:function(a,b){for(var c=0;b>c;c++)this.putBit(1==(1&a>>>b-c-1))},getLengthInBits:function(){return this.length},putBit:function(a){var b=Math.floor(this.length/8);this.buffer.length<=b&&this.buffer.push(0),a&&(this.buffer[b]|=128>>>this.length%8),this.length++}};var l=[[17,14,11,7],[32,26,20,14],[53,42,32,24],[78,62,46,34],[106,84,60,44],[134,106,74,58],[154,122,86,64],[192,152,108,84],[230,180,130,98],[271,213,151,119],[321,251,177,137],[367,287,203,155],[425,331,241,177],[458,362,258,194],[520,412,292,220],[586,450,322,250],[644,504,364,280],[718,560,394,310],[792,624,442,338],[858,666,482,382],[929,711,509,403],[1003,779,565,439],[1091,857,611,461],[1171,911,661,511],[1273,997,715,535],[1367,1059,751,593],[1465,1125,805,625],[1528,1190,868,658],[1628,1264,908,698],[1732,1370,982,742],[1840,1452,1030,790],[1952,1538,1112,842],[2068,1628,1168,898],[2188,1722,1228,958],[2303,1809,1283,983],[2431,1911,1351,1051],[2563,1989,1423,1093],[2699,2099,1499,1139],[2809,2213,1579,1219],[2953,2331,1663,1273]],o=function(){var a=function(a,b){this._el=a,this._htOption=b};return a.prototype.draw=function(a){function g(a,b){var c=document.createElementNS("http://www.w3.org/2000/svg",a);for(var d in b)b.hasOwnProperty(d)&&c.setAttribute(d,b[d]);return c}var b=this._htOption,c=this._el,d=a.getModuleCount();Math.floor(b.width/d),Math.floor(b.height/d),this.clear();var h=g("svg",{viewBox:"0 0 "+String(d)+" "+String(d),width:"100%",height:"100%",fill:b.colorLight});h.setAttributeNS("http://www.w3.org/2000/xmlns/","xmlns:xlink","http://www.w3.org/1999/xlink"),c.appendChild(h),h.appendChild(g("rect",{fill:b.colorDark,width:"1",height:"1",id:"template"}));for(var i=0;d>i;i++)for(var j=0;d>j;j++)if(a.isDark(i,j)){var k=g("use",{x:String(i),y:String(j)});k.setAttributeNS("http://www.w3.org/1999/xlink","href","#template"),h.appendChild(k)}},a.prototype.clear=function(){for(;this._el.hasChildNodes();)this._el.removeChild(this._el.lastChild)},a}(),p="svg"===document.documentElement.tagName.toLowerCase(),q=p?o:m()?function(){function a(){this._elImage.src=this._elCanvas.toDataURL("image/png"),this._elImage.style.display="block",this._elCanvas.style.display="none"}function d(a,b){var c=this;if(c._fFail=b,c._fSuccess=a,null===c._bSupportDataURI){var d=document.createElement("img"),e=function(){c._bSupportDataURI=!1,c._fFail&&_fFail.call(c)},f=function(){c._bSupportDataURI=!0,c._fSuccess&&c._fSuccess.call(c)};return d.onabort=e,d.onerror=e,d.onload=f,d.src="data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",void 0}c._bSupportDataURI===!0&&c._fSuccess?c._fSuccess.call(c):c._bSupportDataURI===!1&&c._fFail&&c._fFail.call(c)}if(this._android&&this._android<=2.1){var b=1/window.devicePixelRatio,c=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(a,d,e,f,g,h,i,j){if("nodeName"in a&&/img/i.test(a.nodeName))for(var l=arguments.length-1;l>=1;l--)arguments[l]=arguments[l]*b;else"undefined"==typeof j&&(arguments[1]*=b,arguments[2]*=b,arguments[3]*=b,arguments[4]*=b);c.apply(this,arguments)}}var e=function(a,b){this._bIsPainted=!1,this._android=n(),this._htOption=b,this._elCanvas=document.createElement("canvas"),this._elCanvas.width=b.width,this._elCanvas.height=b.height,a.appendChild(this._elCanvas),this._el=a,this._oContext=this._elCanvas.getContext("2d"),this._bIsPainted=!1,this._elImage=document.createElement("img"),this._elImage.style.display="none",this._el.appendChild(this._elImage),this._bSupportDataURI=null};return e.prototype.draw=function(a){var b=this._elImage,c=this._oContext,d=this._htOption,e=a.getModuleCount(),f=d.width/e,g=d.height/e,h=Math.round(f),i=Math.round(g);b.style.display="none",this.clear();for(var j=0;e>j;j++)for(var k=0;e>k;k++){var l=a.isDark(j,k),m=k*f,n=j*g;c.strokeStyle=l?d.colorDark:d.colorLight,c.lineWidth=1,c.fillStyle=l?d.colorDark:d.colorLight,c.fillRect(m,n,f,g),c.strokeRect(Math.floor(m)+.5,Math.floor(n)+.5,h,i),c.strokeRect(Math.ceil(m)-.5,Math.ceil(n)-.5,h,i)}this._bIsPainted=!0},e.prototype.makeImage=function(){this._bIsPainted&&d.call(this,a)},e.prototype.isPainted=function(){return this._bIsPainted},e.prototype.clear=function(){this._oContext.clearRect(0,0,this._elCanvas.width,this._elCanvas.height),this._bIsPainted=!1},e.prototype.round=function(a){return a?Math.floor(1e3*a)/1e3:a},e}():function(){var a=function(a,b){this._el=a,this._htOption=b};return a.prototype.draw=function(a){for(var b=this._htOption,c=this._el,d=a.getModuleCount(),e=Math.floor(b.width/d),f=Math.floor(b.height/d),g=['<table style="border:0;border-collapse:collapse;">'],h=0;d>h;h++){g.push("<tr>");for(var i=0;d>i;i++)g.push('<td style="border:0;border-collapse:collapse;padding:0;margin:0;width:'+e+"px;height:"+f+"px;background-color:"+(a.isDark(h,i)?b.colorDark:b.colorLight)+';"></td>');g.push("</tr>")}g.push("</table>"),c.innerHTML=g.join("");var j=c.childNodes[0],k=(b.width-j.offsetWidth)/2,l=(b.height-j.offsetHeight)/2;k>0&&l>0&&(j.style.margin=l+"px "+k+"px")},a.prototype.clear=function(){this._el.innerHTML=""},a}();QRCode=function(a,b){if(this._htOption={width:256,height:256,typeNumber:4,colorDark:"#000000",colorLight:"#ffffff",correctLevel:d.H},"string"==typeof b&&(b={text:b}),b)for(var c in b)this._htOption[c]=b[c];"string"==typeof a&&(a=document.getElementById(a)),this._android=n(),this._el=a,this._oQRCode=null,this._oDrawing=new q(this._el,this._htOption),this._htOption.text&&this.makeCode(this._htOption.text)},QRCode.prototype.makeCode=function(a){this._oQRCode=new b(r(a,this._htOption.correctLevel),this._htOption.correctLevel),this._oQRCode.addData(a),this._oQRCode.make(),this._el.title=a,this._oDrawing.draw(this._oQRCode),this.makeImage()},QRCode.prototype.makeImage=function(){"function"==typeof this._oDrawing.makeImage&&(!this._android||this._android>=3)&&this._oDrawing.makeImage()},QRCode.prototype.clear=function(){this._oDrawing.clear()},QRCode.CorrectLevel=d}(); ]]>
</script>
<style type="text/css"> body{background-color:#fff;font-family:'Tahoma',"Times New Roman",Times,serif;font-size:11px;color:#000}h1,h2{padding-bottom:3px;padding-top:3px;margin-bottom:5px;text-transform:uppercase;font-family:Arial,Helvetica,sans-serif}h1{font-size:1.4em;text-transform:none}h2{font-size:1em;color:brown}h3{font-size:1em;color:#000;text-align:justify;margin:0;padding:0}h4{font-size:1.1em;font-style:bold;font-family:Arial,Helvetica,sans-serif;color:#000;margin:0;padding:0}hr{border:0;color:#9e9e9e;background-color:#9e9e9e;height:1px;width:100%;text-align:left}p,ul,ol{margin-top:1.5em}ul,ol{margin-left:3em}blockquote{margin-left:3em;margin-right:3em;font-style:italic}a{text-decoration:none;color:#70a300}a:hover{border:0;color:#70a300}table{border-spacing:0}.borderRight{border-right:1px solid gray}#despatchTable{border-collapse:collapse;font-size:11px;float:right;border:2px solid black}#ettnTable{border-collapse:collapse;font-size:11px}#customerPartyTable{border-width:0;border-spacing:;border-style:inset;border-collapse:separate;background-color:}#customerIDTable{border-width:2px;border-spacing:;border-style:inset;border-collapse:collapse;background-color:}#customerIDTableTd{border-width:2px;border-spacing:;border-style:inset;border-collapse:collapse;background-color:}#lineTable{border-width:2px;border-spacing:;border-style:inset;border-color:black;border-collapse:collapse}.lineTableTd{border:1px solid black;padding:1px;border-style:inset;background-color:#FFF}#lineTableTr{border-width:1px;padding:0;border-style:inset;border-color:black;background-color:#FFF;-moz-border-radius:5px}#lineTableDummyTd{border-width:1px;border-color:white;padding:1px;border-style:inset;border-color:black;background-color:#FFF}.lineTableBudgetTd{border-width:2px;border-spacing:0;padding:1px;border-style:inset;border-color:black;background-color:#FFF;-moz-border-radius:5px}.notesTable{border:2px solid black}#notesTableTd{border-width:0;border-spacing:;border-style:inset;border-color:black;border-collapse:collapse}.budgetContainerTable{border-width:0;border-spacing:0;border-style:inset;border-color:black;border-collapse:collapse;background-color:#FFF} </style>
<title>e-Arşiv Fatura</title>
</head>
<body style="margin-left=0.6in; margin-right=0.6in; margin-top=0.79in; margin-bottom=0.79in;width:960px;">
<xsl:for-each select="$XML">
<table style="border-color:blue;width:960px;" border="0" cellspacing="0" width="960" cellpadding="0">
<tbody>
<tr valign="top">
<td width="40%" align="center">
<!--  header - sol üst köşe (firma logo ve açıklama)  -->
<img style="width:127px;height:60px;" align="middle" alt="e-Arşiv Logo" src="data:image/png;base64,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"/>
<table align="center" border="0" width="100%">
<tbody>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyName/cbc:Name) != ''">
<tr align="center" valign="top">
<td>
<strong>
<xsl:text>Merkez Adresi :</xsl:text>
</strong>
<br/>
<strong>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyName/cbc:Name)"/>
</strong>
<br/>
</td>
</tr>
</xsl:if>
<xsl:if test="//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:StreetName">
<tr align="center" valign="top">
<td>
<xsl:value-of select="//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:StreetName"/>
<xsl:text> </xsl:text>
<xsl:value-of select="//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:BuildingName"/>
<xsl:text> </xsl:text>
<xsl:text> No: </xsl:text>
<xsl:value-of select="//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:BuildingNumber"/>
<xsl:text> </xsl:text>
<xsl:value-of select="//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:PostalZone"/>
<xsl:text> </xsl:text>
<xsl:value-of select="//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:CitySubdivisionName"/>
<xsl:text> / </xsl:text>
<xsl:value-of select="//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PostalAddress/cbc:CityName"/>
<br/>
<br/>
</td>
</tr>
</xsl:if>
<xsl:if test="//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:Telephone or //n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:Telefax">
<tr align="center" valign="top"> </tr>
</xsl:if>
<xsl:for-each select="//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:Contact/cbc:ElectronicMail">
<tr align="center" valign="top">
<td>
<b>
<xsl:text>E-Posta: </xsl:text>
</b>
<xsl:value-of select="."/>
</td>
</tr>
</xsl:for-each>
<xsl:for-each select="//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:Name">
<tr align="center" valign="top">
<td>
<b>
<xsl:text>Vergi Dairesi: </xsl:text>
</b>
<xsl:value-of select="."/>
</td>
</tr>
</xsl:for-each>
<xsl:for-each select="//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification">
<tr align="center" valign="top">
<td>
<xsl:if test="normalize-space(./cbc:ID/@schemeID) = 'VKN'">
<span>
<b>
<xsl:text>Vergi Numarası: </xsl:text>
</b>
<xsl:value-of select="."/>
</span>
</xsl:if>
</td>
</tr>
</xsl:for-each>
<xsl:for-each select="//n1:Invoice/cac:AccountingSupplierParty/cac:Party/cbc:WebsiteURI">
<tr align="center" valign="top">
<td>
<b>
<xsl:text>Web Sitesi: </xsl:text>
</b>
<xsl:value-of select="."/>
<xsl:text> </xsl:text>
<br/>
<xsl:for-each select="//n1:Invoice/cbc:Note">
<xsl:choose>
<xsl:when test="substring(.,0,6) = 'UPHR:'">
<xsl:value-of select="substring(.,6)"/>
<br/>
</xsl:when>
</xsl:choose>
</xsl:for-each>
</td>
</tr>
</xsl:for-each>
<tr align="center" valign="top">
<td>
<hr/>
<xsl:for-each select="//n1:Invoice/cbc:Note">
<xsl:choose>
<xsl:when test="substring(.,0,5) = 'UPA:'">
<xsl:value-of select="normalize-space(substring(.,5))"/>
<br/>
</xsl:when>
</xsl:choose>
</xsl:for-each>
</td>
</tr>
</tbody>
</table>
</td>
<td width="20%" align="center" valign="center" rowspan="2">
<!--  header - orta kısım (efatura logo)  -->
<center>
<img style="width:91px;" align="middle" alt="E-Fatura Logo" src="data:image/jpeg;base64,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"/>
<h1 align="center">
<span style="font-weight:bold;">e-Arşiv Fatura</span>
</h1>
<img style="width:150px;" align="middle" alt="Imza" src="data:image/jpeg;base64,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"/>
</center>
</td>
<td width="40%" align="center" valign="middle" rowspan="2">
<!--  header - sağ üst köşe  -->
<div id="qrcode"/>
<div id="qrvalue" style="visibility: hidden; height: 20px;width: 20px; ; display:none">
{"vkntckn":"
<xsl:value-of select="n1:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID[@schemeID = 'TCKN' or @schemeID = 'VKN']"/>
", "avkntckn":"
<xsl:value-of select="n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID[@schemeID = 'TCKN' or @schemeID = 'VKN']"/>
<xsl:text> </xsl:text>
", "senaryo":"
<xsl:value-of select="n1:Invoice/cbc:ProfileID"/>
", "tip":"
<xsl:value-of select="n1:Invoice/cbc:InvoiceTypeCode"/>
", "tarih":"
<xsl:value-of select="n1:Invoice/cbc:IssueDate"/>
", "no":"
<xsl:value-of select="n1:Invoice/cbc:ID"/>
", "ettn":"
<xsl:value-of select="n1:Invoice/cbc:UUID"/>
", "parabirimi":"
<xsl:value-of select="n1:Invoice/cbc:DocumentCurrencyCode"/>
", "malhizmettoplam":"
<xsl:value-of select="n1:Invoice/cac:LegalMonetaryTotal/cbc:LineExtensionAmount"/>
<xsl:for-each select="n1:Invoice/cac:TaxTotal/cac:TaxSubtotal[cac:TaxCategory/cac:TaxScheme/cbc:TaxTypeCode = '0015']">
"
<xsl:text>, "kdvmatrah</xsl:text>
(
<xsl:value-of select="cbc:Percent"/>
)":"
<xsl:value-of select="cbc:TaxableAmount"/>
"
</xsl:for-each>
<xsl:for-each select="n1:Invoice/cac:TaxTotal/cac:TaxSubtotal[cac:TaxCategory/cac:TaxScheme/cbc:TaxTypeCode = '0015']">
<xsl:text>, "hesaplanankdv</xsl:text>
(
<xsl:value-of select="cbc:Percent"/>
)":"
<xsl:value-of select="cbc:TaxAmount"/>
",
</xsl:for-each>
"vergidahil":"
<xsl:value-of select="n1:Invoice/cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount"/>
", "odenecek":"
<xsl:value-of select="n1:Invoice/cac:LegalMonetaryTotal/cbc:PayableAmount"/>
"}
</div>
<script type="text/javascript"> var qrcode = new QRCode(document.getElementById("qrcode"), { width : 160, height : 160, correctLevel : QRCode.CorrectLevel.L }); function makeCode (msg) { var elText = document.getElementById("text"); qrcode.makeCode(msg); } makeCode(document.getElementById("qrvalue").innerHTML); </script>
<br/>
<table width="100%" id="despatchTable" border="1">
<xsl:if test="//n1:Invoice/cbc:CustomizationID">
<tr align="left">
<td width="35%">
<span style="font-weight:bold; ">
<xsl:text>Özelleştirme No:</xsl:text>
</span>
</td>
<td width="65%">
<xsl:value-of select="//n1:Invoice/cbc:CustomizationID"/>
</td>
</tr>
</xsl:if>
<xsl:if test="//n1:Invoice/cbc:ProfileID">
<tr align="left">
<td>
<span style="font-weight:bold; ">
<xsl:text>Senaryo:</xsl:text>
</span>
</td>
<td>
<xsl:value-of select="//n1:Invoice/cbc:ProfileID"/>
</td>
</tr>
</xsl:if>
<xsl:if test="//n1:Invoice/cbc:ID">
<tr align="left">
<td>
<span style="font-weight:bold; ">
<xsl:text>Fatura No:</xsl:text>
</span>
</td>
<td>
<xsl:value-of select="//n1:Invoice/cbc:ID"/>
</td>
</tr>
</xsl:if>
<xsl:if test="//n1:Invoice/cbc:InvoiceTypeCode">
<tr align="left">
<td>
<span style="font-weight:bold; ">
<xsl:text>Fatura Tipi:</xsl:text>
</span>
</td>
<td>
<xsl:value-of select="//n1:Invoice/cbc:InvoiceTypeCode"/>
</td>
</tr>
</xsl:if>
<xsl:if test="//n1:Invoice/cac:OrderReference/cbc:ID">
<tr style="height:13px">
<td align="left">
<span style="font-weight:bold; ">
<xsl:text>Sipariş No:</xsl:text>
</span>
</td>
<td align="left">
<xsl:value-of select="//n1:Invoice/cac:OrderReference/cbc:ID"/>
</td>
</tr>
</xsl:if>
<xsl:if test="//n1:Invoice/cac:OrderReference/cbc:IssueDate">
<tr style="height:13px">
<td align="left">
<span style="font-weight:bold; ">
<xsl:text>Sipariş Tarihi:</xsl:text>
</span>
</td>
<td align="left">
<xsl:value-of select="substring(//n1:Invoice/cac:OrderReference/cbc:IssueDate,9,2)"/>
-
<xsl:value-of select="substring(//n1:Invoice/cac:OrderReference/cbc:IssueDate,6,2)"/>
-
<xsl:value-of select="substring(//n1:Invoice/cac:OrderReference/cbc:IssueDate,1,4)"/>
</td>
</tr>
</xsl:if>
<xsl:for-each select="//n1:Invoice/cbc:Note">
<xsl:choose>
<xsl:when test="substring(.,0,11) = 'UPR:Fatura' or substring(.,0,12) = 'UPR: Fatura'">
<tr style="height:13px">
<td align="left">
<span style="font-weight:bold; ">
<xsl:value-of select="normalize-space(substring-before(substring(.,5),':'))"/>
<xsl:text>:</xsl:text>
</span>
</td>
<td align="left">
<xsl:value-of select="normalize-space(substring-after(substring(.,5),':'))"/>
</td>
</tr>
</xsl:when>
</xsl:choose>
</xsl:for-each>
</table>
</td>
</tr>
<tr align="center" valign="top">
<td width="40%" valign="middle" align="center">
<!--  header - sol alt köşe (müşteri bilgileri)  -->
<hr/>
<table id="customerPartyTable" align="center" border="0">
<tbody>
<!--  VKN  -->
<xsl:for-each select="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification">
<xsl:if test="normalize-space(./cbc:ID/@schemeID) = 'VKN'">
<tr>
<td>
<table align="center" border="0">
<tbody>
<tr align="center" valign="top">
<td>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyName/cbc:Name) != ''">
<span style="font-weight:bold; ">
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyName/cbc:Name)"/>
</span>
<br/>
</xsl:if>
</td>
</tr>
<tr align="center" valign="top">
<td>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:StreetName) != ''">
<span>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:StreetName)"/>
</span>
</xsl:if>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BuildingName) != ''">
<span>
<xsl:text> </xsl:text>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BuildingName)"/>
</span>
</xsl:if>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BuildingNumber) != ''">
<span>
<xsl:text> </xsl:text>
<xsl:text>NO: </xsl:text>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BuildingNumber)"/>
</span>
<br/>
</xsl:if>
</td>
</tr>
<tr align="center" valign="top">
<td>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:PostalZone) != ''">
<xsl:text> </xsl:text>
<span>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:PostalZone)"/>
</span>
<xsl:text> </xsl:text>
</xsl:if>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CitySubdivisionName) != ''">
<span>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CitySubdivisionName)"/>
</span>
<xsl:text> / </xsl:text>
</xsl:if>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CityName) != ''">
<span>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CityName)"/>
</span>
<br/>
</xsl:if>
</td>
</tr>
<xsl:for-each select="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:Name">
<tr align="center" valign="top">
<td>
<strong>
<xsl:text>Vergi Dairesi: </xsl:text>
</strong>
<xsl:value-of select="."/>
</td>
</tr>
</xsl:for-each>
<xsl:for-each select="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification">
<xsl:if test="normalize-space(./cbc:ID/@schemeID) = 'VKN'">
<tr align="center" valign="top">
<td>
<strong>
<xsl:text>Vergi Numarası: </xsl:text>
</strong>
<xsl:value-of select="."/>
</td>
</tr>
</xsl:if>
</xsl:for-each>
<xsl:for-each select="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cbc:WebsiteURI">
<xsl:if test="normalize-space(.) != ''">
<tr align="center" valign="top">
<td>
<strong>
<xsl:text>Web Sitesi: </xsl:text>
</strong>
<xsl:value-of select="normalize-space(.)"/>
</td>
</tr>
</xsl:if>
</xsl:for-each>
<xsl:for-each select="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:ElectronicMail">
<xsl:if test="normalize-space(.) != ''">
<tr align="center" valign="top">
<td>
<strong>
<xsl:text>E-Posta: </xsl:text>
</strong>
<xsl:value-of select="normalize-space(.)"/>
</td>
</tr>
</xsl:if>
</xsl:for-each>
<xsl:if test="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telephone or //n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telefax"> </xsl:if>
</tbody>
</table>
</td>
</tr>
</xsl:if>
</xsl:for-each>
<!--  tckn  -->
<xsl:for-each select="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification">
<xsl:if test="normalize-space(./cbc:ID/@schemeID) = 'TCKN'">
<tr>
<td>
<table align="center" border="0">
<tbody>
<tr align="center" valign="top">
<td>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Person/cbc:FirstName) != ''">
<span style="font-weight:bold; ">
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Person/cbc:FirstName)"/>
<xsl:text> </xsl:text>
</span>
</xsl:if>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Person/cbc:MiddleName) != ''">
<span style="font-weight:bold; ">
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Person/cbc:MiddleName)"/>
<xsl:text> </xsl:text>
</span>
</xsl:if>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Person/cbc:FamilyName) != ''">
<span style="font-weight:bold; ">
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Person/cbc:FamilyName)"/>
</span>
<br/>
</xsl:if>
</td>
</tr>
<tr align="center" valign="top">
<td>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:StreetName) != ''">
<span>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:StreetName)"/>
</span>
</xsl:if>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BuildingName) != ''">
<span>
<xsl:text> </xsl:text>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BuildingName)"/>
</span>
</xsl:if>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BuildingNumber) != ''">
<span>
<xsl:text> </xsl:text>
<xsl:text>NO: </xsl:text>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:BuildingNumber)"/>
</span>
<br/>
</xsl:if>
</td>
</tr>
<tr align="center" valign="top">
<td>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:PostalZone) != ''">
<xsl:text> </xsl:text>
<span>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:PostalZone)"/>
</span>
<xsl:text> </xsl:text>
</xsl:if>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CitySubdivisionName) != ''">
<span>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CitySubdivisionName)"/>
</span>
<xsl:text> / </xsl:text>
</xsl:if>
<xsl:if test="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CityName) != ''">
<span>
<xsl:value-of select="normalize-space(//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PostalAddress/cbc:CityName)"/>
</span>
<br/>
</xsl:if>
</td>
</tr>
<xsl:for-each select="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyTaxScheme/cac:TaxScheme/cbc:Name">
<tr align="center" valign="top">
<td>
<strong>
<xsl:text>Vergi Dairesi: </xsl:text>
</strong>
<xsl:value-of select="."/>
</td>
</tr>
</xsl:for-each>
<xsl:for-each select="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification">
<xsl:if test="normalize-space(./cbc:ID/@schemeID) = 'TCKN'">
<tr align="center" valign="top">
<td>
<strong>
<xsl:text>Kimlik Numarası: </xsl:text>
</strong>
<xsl:value-of select="."/>
</td>
</tr>
</xsl:if>
</xsl:for-each>
<xsl:for-each select="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cbc:WebsiteURI">
<xsl:if test="normalize-space(.) != ''">
<tr align="center" valign="top">
<td>
<strong>
<xsl:text>Web Sitesi: </xsl:text>
</strong>
<xsl:value-of select="normalize-space(.)"/>
</td>
</tr>
</xsl:if>
</xsl:for-each>
<xsl:for-each select="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:ElectronicMail">
<xsl:if test="normalize-space(.) != ''">
<tr align="center" valign="top">
<td>
<strong>
<xsl:text>E-Posta: </xsl:text>
</strong>
<xsl:value-of select="normalize-space(.)"/>
</td>
</tr>
</xsl:if>
</xsl:for-each>
<xsl:if test="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telephone or //n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telefax">
<tr align="center" valign="top">
<td>
<xsl:if test="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telephone">
<strong>
<xsl:text>Tel: </xsl:text>
</strong>
<xsl:value-of select="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telephone"/>
<xsl:text> </xsl:text>
</xsl:if>
<xsl:if test="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telefax">
<strong>
<xsl:text>Faks: </xsl:text>
</strong>
<xsl:value-of select="//n1:Invoice/cac:AccountingCustomerParty/cac:Party/cac:Contact/cbc:Telefax"/>
</xsl:if>
</td>
</tr>
</xsl:if>
</tbody>
</table>
</td>
</tr>
</xsl:if>
</xsl:for-each>
</tbody>
</table>
</td>
</tr>
<tr align="left">
<table id="ettnTable" width="960">
<tr>
<td align="left" width="50%" valign="bottom">
<xsl:for-each select="//n1:Invoice/cbc:Note">
<xsl:choose>
<xsl:when test="substring(.,0,5) = 'UPL:'">
<xsl:value-of select="substring(.,5)"/>
<br/>
</xsl:when>
</xsl:choose>
</xsl:for-each>
<br/>
<xsl:text>ETTN: </xsl:text>
<xsl:value-of select="//n1:Invoice/cbc:UUID"/>
</td>
</tr>
</table>
</tr>
</tbody>
</table>
<div id="lineTableAligner">
<span>
<xsl:text> </xsl:text>
</span>
</div>
<table border="1" id="lineTable" width="960">
<tbody>
<tr id="lineTableTr">
<td class="lineTableTd" align="center" width="10%">
<span style="font-weight:bold; ">
<xsl:text>Malzeme Kodu/Code</xsl:text>
</span>
</td>
<td class="lineTableTd" align="center" width="55%">
<span style="font-weight:bold; ">
<xsl:text>Açıklama/Description</xsl:text>
</span>
</td>
<td class="lineTableTd" align="center" width="15%">
<span style="font-weight:bold; ">
<xsl:text>Miktar/Quantity</xsl:text>
</span>
</td>
<td class="lineTableTd" align="center" width="15%">
<span style="font-weight:bold; ">
<xsl:text>Fiyat/Price</xsl:text>
</span>
</td>
<td class="lineTableTd" align="center" width="15%">
<span style="font-weight:bold; ">
<xsl:text>İskonto/Discount</xsl:text>
</span>
</td>
<td class="lineTableTd" align="center" width="15%">
<span style="font-weight:bold; ">
<xsl:text>KDV</xsl:text>
</span>
</td>
<td class="lineTableTd" align="center" width="15%">
<span style="font-weight:bold; ">
<xsl:text>Tutarı/Amount</xsl:text>
</span>
</td>
</tr>
<xsl:for-each select="//n1:Invoice/cac:InvoiceLine">
<xsl:choose>
<xsl:when test=".">
<xsl:apply-templates select="."/>
</xsl:when>
<xsl:otherwise>
<xsl:apply-templates select="//n1:Invoice"/>
</xsl:otherwise>
</xsl:choose>
</xsl:for-each>
</tbody>
</table>
</xsl:for-each>
<table class="budgetContainerTable" style="margin-top:10px;">
<tr>
<td>
<table class="budgetContainerTable" width="620" style="width:620px;">
<tr class="budgetContainerTr">
<td>
<xsl:for-each select="//n1:Invoice/cbc:Note">
<xsl:choose>
<xsl:when test="substring(.,0,5) = 'MIL:'">
<xsl:value-of select="substring(.,5)"/>
<br/>
</xsl:when>
</xsl:choose>
</xsl:for-each>
</td>
</tr>
</table>
</td>
<td>
<table class="budgetContainerTable" width="337" style="width:337px;">
<tr class="budgetContainerTr" align="right">
<td class="lineTableBudgetTd" align="right" width="270" style="width:270px;">
<strong>
<xsl:text>Toplam Tutar:</xsl:text>
</strong>
</td>
<td class="lineTableBudgetTd" width="101" style="width:101px;" align="right">
<xsl:for-each select="n1:Invoice/cac:LegalMonetaryTotal/cbc:LineExtensionAmount">
<xsl:call-template name="Curr_Type"/>
</xsl:for-each>
</td>
</tr>
<tr class="budgetContainerTr" align="right">
<td class="lineTableBudgetTd" align="right" width="270" style="width:270px;">
<strong>
<xsl:text>Toplam İskonto:</xsl:text>
</strong>
</td>
<td class="lineTableBudgetTd" width="101" style="width:101px;" align="right">
<xsl:choose>
<xsl:when test="n1:Invoice/cac:LegalMonetaryTotal/cbc:AllowanceTotalAmount">
<xsl:for-each select="n1:Invoice/cac:LegalMonetaryTotal/cbc:AllowanceTotalAmount">
<xsl:call-template name="Curr_Type"/>
</xsl:for-each>
</xsl:when>
<xsl:otherwise>
<xsl:text>0 TL</xsl:text>
</xsl:otherwise>
</xsl:choose>
</td>
</tr>
<xsl:for-each select="n1:Invoice/cac:TaxTotal/cac:TaxSubtotal">
<tr class="budgetContainerTr" align="right"> </tr>
<td class="lineTableBudgetTd" align="right" width="270" style="width:270px;">
<strong>
<xsl:text>Hesaplanan </xsl:text>
<xsl:value-of select="cac:TaxCategory/cac:TaxScheme/cbc:Name"/>
<xsl:text> (</xsl:text>
<xsl:value-of select="cbc:TaxableAmount"/>
<xsl:text>) </xsl:text>
<xsl:text> %</xsl:text>
<xsl:value-of select="cbc:Percent"/>
<xsl:text>:</xsl:text>
</strong>
</td>
<td class="lineTableBudgetTd" width="101" style="width:101px;" align="right">
<xsl:for-each select="cac:TaxCategory/cac:TaxScheme">
<xsl:text> </xsl:text>
<xsl:value-of select="format-number(../../cbc:TaxAmount, '###.##0,00', 'european')"/>
<xsl:if test="../../cbc:TaxAmount/@currencyID">
<xsl:text> </xsl:text>
<xsl:if test="../../cbc:TaxAmount/@currencyID = 'TRL' or ../../cbc:TaxAmount/@currencyID = 'TRY'">
<xsl:text>TL</xsl:text>
</xsl:if>
<xsl:if test="../../cbc:TaxAmount/@currencyID != 'TRL' and ../../cbc:TaxAmount/@currencyID != 'TRY'">
<xsl:value-of select="../../cbc:TaxAmount/@currencyID"/>
</xsl:if>
</xsl:if>
</xsl:for-each>
</td>
</xsl:for-each>
<tr class="budgetContainerTr" align="right">
<td class="lineTableBudgetTd" align="right" width="270" style="width:270px;">
<strong>
<xsl:text>Fatura Tutarı:</xsl:text>
</strong>
</td>
<td class="lineTableBudgetTd" width="101" style="width:101px;" align="right">
<xsl:for-each select="n1:Invoice/cac:LegalMonetaryTotal/cbc:PayableAmount">
<xsl:call-template name="Curr_Type"/>
</xsl:for-each>
</td>
</tr>
</table>
</td>
</tr>
</table>
<table class="notesTable" width="960" align="left" height="50" cellpadding="2" cellspacing="2" style="margin-top:10px;margin-bottom:10px;width:960px;text-align:left;">
<tr>
<td id="notesTableTd">
<div class="clear"/>
<table style="width:100%;text-align:left;float:left;" width="100%" align="left" cellpadding="2" cellspacing="2">
<xsl:for-each select="//n1:Invoice/cbc:Note">
<xsl:choose>
<xsl:when test="substring(.,0,5) = 'N2C:'">
<tr align="left">
<td style="width:50%;text-align:left;">
<xsl:value-of select="substring-before(substring(.,5),'!#')"/>
</td>
<td style="width:50%;text-align:left;">
<xsl:value-of select="substring-after(substring(.,5),'!#')"/>
</td>
</tr>
</xsl:when>
<xsl:when test="substring(.,0,13) = ':N2C-AYIRAC:'">
<tr align="left">
<td colspan="2">
<hr/>
</td>
</tr>
</xsl:when>
</xsl:choose>
</xsl:for-each>
</table>
<div class="clear"/>
<div style="width:100%;text-align:left;float:left;">
<xsl:for-each select="//n1:Invoice/cbc:Note">
<xsl:choose>
<xsl:when test="substring(.,0,5) = 'NOT:'">
<xsl:value-of select="substring(.,5)"/>
<br/>
</xsl:when>
<xsl:when test="substring(.,0,13) = ':NOT-AYIRAC:'">
<hr/>
</xsl:when>
<xsl:when test="substring(.,0,6) = 'IMEI:'">
<xsl:value-of select="."/>
<br/>
</xsl:when>
</xsl:choose>
</xsl:for-each>
</div>
<div class="clear"/>
</td>
</tr>
</table>
</body>
</html>
</xsl:template>
<xsl:template match="dateFormatter">
<xsl:value-of select="substring(.,9,2)"/>
-
<xsl:value-of select="substring(.,6,2)"/>
-
<xsl:value-of select="substring(.,1,4)"/>
</xsl:template>
<xsl:template match="//n1:Invoice/cac:InvoiceLine">
<tr id="lineTableTr">
<td class="lineTableTd" align="center">
<span>
<xsl:text> </xsl:text>
<xsl:value-of select="./cac:Item/cac:SellersItemIdentification/cbc:ID"/>
</span>
</td>
<td class="lineTableTd" align="left">
<span>
<xsl:text>    </xsl:text>
<xsl:value-of select="./cac:Item/cbc:Name"/>
</span>
</td>
<td class="lineTableTd" align="center">
<span>
<xsl:text> </xsl:text>
<xsl:value-of select="format-number(./cbc:InvoicedQuantity, '###.##0,####', 'european')"/>
<xsl:text> </xsl:text>
<xsl:if test="./cbc:InvoicedQuantity/@unitCode">
<xsl:for-each select="./cbc:InvoicedQuantity">
<xsl:text> </xsl:text>
<xsl:choose>
<xsl:when test="@unitCode = '26'">
<span>
<xsl:text>Ton</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'BX'">
<span>
<xsl:text>Kutu</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'LTR'">
<span>
<xsl:text>LT</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'NIU'">
<span>
<xsl:text>Adet</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'KGM'">
<span>
<xsl:text>KG</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'KJO'">
<span>
<xsl:text>kJ</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'GRM'">
<span>
<xsl:text>G</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'MGM'">
<span>
<xsl:text>MG</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'GT'">
<span>
<xsl:text>GT</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'MTR'">
<span>
<xsl:text>M</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'MMT'">
<span>
<xsl:text>MM</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'KTM'">
<span>
<xsl:text>KM</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'MLT'">
<span>
<xsl:text>ML</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'MMQ'">
<span>
<xsl:text>MM3</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'CLT'">
<span>
<xsl:text>CL</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'CMK'">
<span>
<xsl:text>CM2</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'CMQ'">
<span>
<xsl:text>CM3</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'CMT'">
<span>
<xsl:text>CM</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'MTK'">
<span>
<xsl:text>M2</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'MTQ'">
<span>
<xsl:text>M3</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'DAY'">
<span>
<xsl:text> Gün</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'PA'">
<span>
<xsl:text> Paket</xsl:text>
</span>
</xsl:when>
<xsl:when test="@unitCode = 'PK'">
<span>
<xsl:text>KL</xsl:text>
</span>
</xsl:when>
</xsl:choose>
</xsl:for-each>
</xsl:if>
</span>
</td>
<td class="lineTableTd" align="right">
<span>
<xsl:text> </xsl:text>
<xsl:value-of select="format-number(./cac:Price/cbc:PriceAmount, '###.##0,####', 'european')"/>
<xsl:text> </xsl:text>
<xsl:if test="./cac:Price/cbc:PriceAmount/@currencyID">
<xsl:text/>
<xsl:if test="./cac:Price/cbc:PriceAmount/@currencyID = "TRL" or ./cbc:LineExtensionAmount/@currencyID = "TRY"">
<xsl:text>TL</xsl:text>
</xsl:if>
<xsl:if test="./cac:Price/cbc:PriceAmount/@currencyID != "TRL" and ./cbc:LineExtensionAmount/@currencyID != "TRY"">
<xsl:value-of select="./cac:Price/cbc:PriceAmount/@currencyID"/>
</xsl:if>
</xsl:if>
</span>
</td>
<td class="lineTableTd" align="right">
<span>
<xsl:choose>
<xsl:when test="cac:AllowanceCharge/cbc:Amount">
<xsl:text> </xsl:text>
<xsl:value-of select="format-number(./cac:AllowanceCharge/cbc:Amount, '###.##0,####', 'european')"/>
<xsl:text> </xsl:text>
<xsl:if test="./cac:AllowanceCharge/cbc:Amount/@currencyID">
<xsl:text/>
<xsl:if test="./cac:AllowanceCharge/cbc:Amount/@currencyID = "TRL" or ./cac:AllowanceCharge/cbc:Amount/@currencyID = "TRY"">
<xsl:text>TL</xsl:text>
</xsl:if>
<xsl:if test="./cac:AllowanceCharge/cbc:Amount/@currencyID != "TRL" and ./cac:AllowanceCharge/cbc:Amount/@currencyID != "TRY"">
<xsl:value-of select="./cac:AllowanceCharge/cbc:Amount/@currencyID"/>
</xsl:if>
</xsl:if>
</xsl:when>
<xsl:otherwise>
<xsl:text>0 TL</xsl:text>
</xsl:otherwise>
</xsl:choose>
</span>
</td>
<td class="lineTableTd" align="right">
<xsl:for-each select="./cac:TaxTotal/cac:TaxSubtotal">
<span>
<xsl:text>%</xsl:text>
<xsl:value-of select="cbc:Percent"/>
</span>
</xsl:for-each>
</td>
<td class="lineTableTd" align="right">
<span>
<xsl:value-of select="format-number(./cbc:LineExtensionAmount, '###.##0,####', 'european')"/>
<xsl:text> </xsl:text>
<xsl:if test="./cbc:LineExtensionAmount/@currencyID">
<xsl:text/>
<xsl:if test="./cbc:LineExtensionAmount/@currencyID = "TRL" or ./cbc:LineExtensionAmount/@currencyID = "TRY"">
<xsl:text>TL</xsl:text>
</xsl:if>
<xsl:if test="./cbc:LineExtensionAmount/@currencyID != "TRL" and ./cbc:LineExtensionAmount/@currencyID != "TRY"">
<xsl:value-of select="./cbc:LineExtensionAmount/@currencyID"/>
</xsl:if>
</xsl:if>
</span>
</td>
</tr>
</xsl:template>
<xsl:template name="Curr_Type">
<xsl:value-of select="format-number(., '###.##0,00', 'european')"/>
<xsl:if test="@currencyID">
<xsl:text> </xsl:text>
<xsl:choose>
<xsl:when test="@currencyID = 'TRL' or @currencyID = 'TRY'">
<xsl:text>TL</xsl:text>
</xsl:when>
<xsl:otherwise>
<xsl:value-of select="@currencyID"/>
</xsl:otherwise>
</xsl:choose>
</xsl:if>
</xsl:template>
</xsl:stylesheet>