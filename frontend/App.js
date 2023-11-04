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
      <View style={styles.toolbarView}></View>
     <ScrollView style={styles.buttonListView}></ScrollView>
      <Appbar
      
          
        >
        <Appbar.Action icon="archive" onPress={() => {}} />
        <Appbar.Action icon="email" onPress={() => {}} />
        <Appbar.Action icon="label" onPress={() => {}} />
        <Appbar.Action icon="delete" onPress={() => {}} /> 
         <FAB
          mode="flat"
          size="medium"
          icon="plus"
          onPress={() => {}}
          style={[
            styles.fab,
            { top: (BOTTOM_APPBAR_HEIGHT - MEDIUM_FAB_HEIGHT) / 2 },
          ]}
        />
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
  bottom: {
    backgroundColor: 'aquamarine',
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
  },
  fab: {
    position: 'absolute',
    right: 16,
  },
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
