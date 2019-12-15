<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" minScale="1e+08" hasScaleBasedVisibilityFlag="0" version="3.8.2-Zanzibar" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property value="Value" key="identify/format"/>
  </customproperties>
  <pipe>
    <rasterrenderer opacity="1" classificationMax="2" band="1" alphaBand="-1" type="singlebandpseudocolor" classificationMin="-5">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader classificationMode="2" clip="0" colorRampType="INTERPOLATED">
          <colorramp name="[source]" type="gradient">
            <prop k="color1" v="43,131,186,255"/>
            <prop k="color2" v="215,25,28,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.25;171,221,164,255:0.5;255,255,191,255:0.75;253,174,97,255"/>
          </colorramp>
          <item value="-5" alpha="255" label="-5" color="#2b83ba"/>
          <item value="-3.8" alpha="255" label="-3.8" color="#83c1ab"/>
          <item value="-2.5" alpha="255" label="-2.5" color="#cfecb0"/>
          <item value="-1.5" alpha="255" label="-1.5" color="#ffffbf"/>
          <item value="-0.4" alpha="255" label="-0.4" color="#fecc84"/>
          <item value="0.8" alpha="255" label="0.8" color="#f27f4b"/>
          <item value="2" alpha="255" label="2" color="#d7191c"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0"/>
    <huesaturation colorizeOn="0" colorizeBlue="128" colorizeRed="255" colorizeGreen="128" grayscaleMode="0" saturation="0" colorizeStrength="100"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
