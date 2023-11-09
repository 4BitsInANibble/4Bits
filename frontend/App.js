import { StatusBar } from 'expo-status-bar';
import { SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import React, { Component } from 'react';
import { Appbar, FAB, useTheme } from 'react-native-paper';
import {useSafeAreaInsets, SafeAreaProvider} from 'react-native-safe-area-context';

const BOTTOM_APPBAR_HEIGHT = 80;
const MEDIUM_FAB_HEIGHT = 56;

const App = () => {
  
  // const { bottom } = useSafeAreaInsets();
  const theme = useTheme();

  return (
    <SafeAreaProvider>
    <SafeAreaView>

        <Appbar style={styles.item} >  
        <Appbar.Action size= {30} color= 'orange' icon="home" onPress={() => {}} />
        <Appbar.Action size= {30} color= 'orange' icon="scan-helper" onPress={() => {}} /> 
        <Appbar.Action size= {30} color= 'orange' icon="fridge-bottom" onPress={() => {}} />
        <Appbar.Action size= {30} color= 'orange' icon="cart-heart" onPress={() => {}} />
        <Appbar.Action size= {30} color= 'orange' icon="account" onPress={() => {}} /> 
        
        </Appbar> 

    </SafeAreaView>
    </SafeAreaProvider>
  );
    
};

// const Toolbar = () => {
//   return <SafeAreaView style={styles.container}>
//     <View style={styles.toolbarView}></View>
//   </SafeAreaView>
// }

const styles = StyleSheet.create({
  item: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  }
});

export default App;


// export default function App() {
//   return (
//   <SafeAreaView style={styles.container}>
//     <View style={styles.toolbarView}></View>
//     <ScrollView style={styles.buttonListView}></ScrollView>
//   </SafeAreaView>
//   );
// }

// const styles = StyleSheet.create({
//   toolbarView: {
//     width: 340,
//     height: 66,
//     backgroundColor: 'white',
//     shadowColor: 'grey',
//     shadowOffset: {width: 0, height: 8},
//     shadowOpacity: 0.4,
//     shadowRadius: 10,
//     borderRadius: 12,
//     marginHorizontal: 24,
//     marginVertical: 40,
//   },
//   buttonListView:{
//     position:'absolute',
//     height: 66,
//     width: '100%',
//     marginHorizontal: 24,
//     marginVertical: 40,
//   }
// });
  // container: {
  //   flex: 1,
  //   backgroundColor: '#f5f5dc',
  //   alignItems: 'center',
  //   justifyContent: 'center',
  // },
